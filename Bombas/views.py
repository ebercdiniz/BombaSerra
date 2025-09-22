from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Mode
from django.utils import timezone
import logging


# Função auxiliar para calcular o estado dos pinos
def compute_pins(mode):
    pins = {'21': 0, '5': 0, '18': 0, '19': 0}
    if mode == 'ronaldo':
        pins['21'] = 1
    elif mode == 'nene':
        pins['21'] = 1
        pins['5'] = 1
        pins['18'] = 1
    elif mode == 'eber':
        pins['21'] = 1
        pins['5'] = 1
        pins['19'] = 1
    return pins


# Página principal (usando TemplateView)
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Mode.objects.get_or_create(pk=1)
        current = Mode.objects.get(pk=1)
        context['mode'] = current.mode
        return context


# API para obter estado atual
# API para o ESP32 enviar ping
@api_view(['POST'])
def esp32_ping(request):
    obj, _ = Mode.objects.get_or_create(pk=1)
    obj.last_ping = timezone.now()  # <-- atualiza hora do último ping
    obj.save()
    return Response({'status': 'ok'})

@api_view(['GET'])
def get_state(request):
    try:
        logging.warning("Get")
        obj, _ = Mode.objects.get_or_create(pk=1)
        obj.last_ping = timezone.now()
        obj.save(update_fields=['last_ping'])
        pins = compute_pins(obj.mode)
        delta = (timezone.now() - obj.last_ping).total_seconds() if obj.last_ping else 9999
        esp32_online = delta < 30  # 30s de timeout
        return Response({
            'mode': obj.mode,
            'pins': pins,
            'esp32_online': esp32_online
        })
    except Exception as e:
        logging.error(f"Erro ao obter estado: {e}")
        return Response({'mode': 'none', 'pins': {}, 'esp32_online': False},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API para definir o modo
@api_view(['POST'])
def set_mode(request):
    mode = request.data.get('mode')
    if mode not in ['none', 'ronaldo', 'nene', 'eber']:
        return Response({'detail': 'invalid mode'}, status=status.HTTP_400_BAD_REQUEST)

    obj, _ = Mode.objects.get_or_create(pk=1)
    obj.mode = mode
    obj.save()
    logging.warning("Pinos")
    pins = compute_pins(mode)
    logging.warning(pins)
    return Response({'mode': mode, 'pins': pins})
