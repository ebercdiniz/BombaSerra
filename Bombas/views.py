from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Mode

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
@api_view(['GET'])
def get_state(request):
    logging.warning("Get")
    obj, _ = Mode.objects.get_or_create(pk=1)
    pins = compute_pins(obj.mode)
    return Response({'mode': obj.mode, 'pins': pins})


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
