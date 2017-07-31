# coding: utf-8
"""Sincroniza as informações"""
import datetime

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator

from detransapp.rest import JSONResponse
from detransapp.decorators import validar_imei


class SincronismoRestView(APIView):
    """View para sincronizar"""
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        """envia para o servidor a data de agora"""
        return JSONResponse({'data': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
