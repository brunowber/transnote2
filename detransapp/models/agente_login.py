# coding: utf-8
"""Model para login de agentes"""

from django.db import models
from detransapp.models.agente import Agente
from detransapp.models.dispositivo import Dispositivo


class Agente_login(models.Model):
    """Classe para model de login de agentes"""

    device = models.ForeignKey(Dispositivo)
    agente = models.ForeignKey(Agente)
    status = models.BooleanField(default=False)
    data_login = models.DateTimeField(auto_now_add=True)
    data_logout = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __unicode__(self):
        return self.agente.username

    class Meta:
        app_label = "detransapp"

