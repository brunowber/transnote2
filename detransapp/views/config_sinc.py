# coding: utf-8
"""Arquivo para configuraçao de sincronização"""

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.config_sinc import FormConfigSinc
from detransapp.models import ConfigSinc
from detransapp.decorators import validar_imei
from detransapp.rest import JSONResponse
from detransapp.serializers import ConfigSincSerializer


class ConfigSincView(View):
    """View para configurar a sincronização"""

    template = 'config/configuracao.html'

    def get(self, request, config_sinc_id=None):
        """Pega um formulário de sincronização e envia para o template"""

        if config_sinc_id:
            config_sinc = ConfigSinc.objects.get(pk=config_sinc_id)
            form = FormConfigSinc(instance=config_sinc)
        else:
            form = FormConfigSinc()

        return render(request, self.template, {'form': form})

    def post(self, request, config_sinc_id=None):
        """Envia o formulário para o servidor"""

        if config_sinc_id:
            config_sinc = ConfigSinc.objects.get(pk=config_sinc_id)
            form = FormConfigSinc(instance=config_sinc, data=request.POST)
        else:

            form = FormConfigSinc(request.POST)

        if form.is_valid():
            form.save(request)

            return redirect('/')

        return render(request, self.template, {'form': form})


class GetConfigSincRestView(APIView):
    """Pega os arquivos de configuração do servidor no Android"""

    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        """Pega as configurações e envia para o servidor"""
        if 'data' in request.POST:
            config_sinc = ConfigSinc.objects.get_config_sinc_sicronismo(request.POST['data'])
        else:
            config_sinc = ConfigSinc.objects.get_config_sinc_sicronismo()

        serializer = ConfigSincSerializer(config_sinc)

        return JSONResponse(serializer.data)
