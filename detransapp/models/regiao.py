# coding: utf-8
"""Model para regiões"""

from django.db import models
from detransapp.manager import RegiaoManager


class Regiao(models.Model):
    """Classe para model de regiões"""

    nome = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)
    objects = RegiaoManager()

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = "detransapp"
