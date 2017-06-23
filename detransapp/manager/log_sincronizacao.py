# coding: utf-8
"""gerencia os logs de sincronização"""

from django.db import models


class LogSincronizacaoManager(models.Manager):
    """Classe para gerenciar os logs de sincronização"""

    def registrar(self, imei, usuario_id, solicitacao):
        from detransapp.models import Dispositivo
        registro = self.model()

        registro.dispositivo_id = Dispositivo.objects.filter(imei=str(imei)).get().id
        registro.usuario_id = usuario_id
        registro.solicitacao = solicitacao
        registro.save()
