from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Mode, Schedule
from django.utils import timezone
from datetime import timedelta
import logging


# Função auxiliar para calcular o estado dos pinos
def compute_pins(mode):

    pins = {'21': 1, '5': 0, '18': 0, '19': 0}

    # =========================
    # MODO MANUAL (já existente)
    # =========================
    if mode == 'eber':

        obj = Mode.objects.get(pk=1)

        if (
                obj.manual_until is not None and
                timezone.now() >= obj.manual_until
        ):
            obj.mode = "none"
            obj.manual_until = None
            obj.save(update_fields=[
                "mode",
                "manual_until"
            ])
        else:
            pins["21"] = 0
            return pins


    # =========================
    # MODO AUTOMÁTICO
    # =========================

    now = timezone.localtime()

    weekday = now.weekday()

    current_time = now.time()

    schedules = Schedule.objects.filter(
        weekday=weekday
    )

    for schedule in schedules:

        if (
            schedule.start_time <= current_time <
            schedule.end_time
        ):

            if schedule.mode == 'eber':

                pins['21'] = 0

            break

    return pins


# Página principal
class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        Mode.objects.get_or_create(pk=1)

        current = Mode.objects.get(pk=1)

        context['mode'] = current.mode

        context['schedules'] = Schedule.objects.all().order_by(
            'weekday',
            'start_time'
        )

        return context


# API para o ESP32 enviar ping
@api_view(['POST'])
def esp32_ping(request):

    obj, _ = Mode.objects.get_or_create(pk=1)

    obj.save(update_fields=['last_ping'])

    return Response({'status': 'ok'})


@api_view(['GET'])
def esp32_state(request):

    try:

        obj, _ = Mode.objects.get_or_create(pk=1)

        now = timezone.localtime()

        current_weekday = now.weekday()

        current_time = now.time()

        automatic_active = False

        schedules = Schedule.objects.filter(
            weekday=current_weekday
        )

        for s in schedules:

            if s.start_time <= current_time <= s.end_time:

                automatic_active = True
                break

        # ==========================================
        # CONTROLE AUTOMÁTICO
        # ==========================================

        if automatic_active:

            obj.mode = 'eber'
            obj.auto_active = True

        else:

            # só desliga se quem ligou foi o automático

            if obj.auto_active:

                obj.mode = 'none'
                obj.auto_active = False

        obj.last_ping = timezone.now()

        obj.save(update_fields=[
            'mode',
            'auto_active',
            'last_ping'
        ])

        pins = compute_pins(obj.mode)

        return Response({
            'mode': obj.mode,
            'pins': pins,
            'esp32_online': True
        })

    except Exception as e:

        logging.error(f"Erro no esp32_state: {e}")

        return Response({
            'mode': 'none',
            'pins': {},
            'esp32_online': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API para obter estado atual
@api_view(['GET'])
def get_state(request):

    try:

        obj, _ = Mode.objects.get_or_create(pk=1)

        pins = compute_pins(obj.mode)

        delta = (
            timezone.now() - obj.last_ping
        ).total_seconds() if obj.last_ping else 9999

        esp32_online = delta < 30

        server_time = timezone.localtime().strftime("%H:%M:%S")

        return Response({
            'mode': obj.mode,
            'pins': pins,
            'esp32_online': esp32_online,
            'server_time': server_time
        })

    except Exception as e:

        logging.error(f"Erro ao obter estado: {e}")

        return Response({
            'mode': 'none',
            'pins': {},
            'esp32_online': False,
            'server_time': '--:--:--'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API para definir o modo
@api_view(['POST'])
def set_mode(request):

    mode = request.data.get('mode')

    if mode not in ['none', 'ligar', 'nene', 'eber']:

        return Response({
            'detail': 'invalid mode'
        }, status=status.HTTP_400_BAD_REQUEST)

    obj, _ = Mode.objects.get_or_create(pk=1)

    obj.mode = mode

    if mode == "eber":
        obj.manual_until = timezone.now() + timedelta(hours=1)
    else:
        obj.manual_until = None

    obj.save(update_fields=[
        "mode",
        "manual_until"
    ])

    pins = compute_pins(mode)

    return Response({
        'mode': mode,
        'pins': pins
    })


# Adicionar programação
@api_view(['POST'])
def add_schedule(request):

    weekday = request.data.get('weekday')

    start_time = request.data.get('start_time')

    end_time = request.data.get('end_time')

    Schedule.objects.create(
        weekday=weekday,
        start_time=start_time,
        end_time=end_time,
        mode='eber'
    )

    return Response({'status': 'ok'})


# Apagar programação
@api_view(['POST'])
def delete_schedule(request):

    schedule_id = request.data.get('id')

    Schedule.objects.filter(id=schedule_id).delete()

    return Response({'status': 'deleted'})

