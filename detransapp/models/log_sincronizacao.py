# coding: utf-8
"""Model para logs de sincronizações"""

from django.db import models
from django.contrib.auth.models import User
from detransapp.models import Dispositivo
from detransapp.manager import LogSincronizacaoManager


class LogSincronizacao(models.Model):
    """Classe para logs de sincronização"""

    dispositivo = models.ForeignKey(Dispositivo)
    usuario = models.ForeignKey(User)
    data = models.DateTimeField(auto_now_add=True)
    solicitacao = models.IntegerField(choices=((0, 'Download'),
                                               (1, 'Parcial'), (2, 'Recebimento infração')))

    objects = LogSincronizacaoManager()

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        app_label = "detransapp"
