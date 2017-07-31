# coding: utf-8
"""Model para bloco padrão"""

from django.db import models
from detransapp.manager import BlocoManager


class BlocoPadrao(models.Model):
    """Classe para model do bloco padrão"""

    inicio_intervalo = models.IntegerField()
    fim_intervalo = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    contador = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    numero_paginas = models.IntegerField(default=1000)
    minimo_pag_restantes = models.IntegerField(null=True)

    objects = BlocoManager()

    def __unicode__(self):
        return str(self.pk)
