# coding: utf-8
"""Model para blocos"""

from django.db import models
from django.contrib.auth.models import User
from detransapp.manager import BlocoManager
from detransapp.models.agente import Agente
from detransapp.models.bloco_padrao import BlocoPadrao


class Bloco(models.Model):
    """Classe para models de blocos"""

    inicio_intervalo = models.PositiveIntegerField()
    fim_intervalo = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User)
    agente_campo = models.ForeignKey(Agente, null=True, blank=True, related_name='+')
    ativo = models.BooleanField(default=True)
    minimo_pag_restantes = models.IntegerField(null=True)
    bloco_padrao = models.ForeignKey(BlocoPadrao, null=True)

    objects = BlocoManager()

    def __unicode__(self):
        return self.usuario.first_name
