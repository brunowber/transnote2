# coding: utf-8
"""Model para DETs"""

from django.db import models
from detransapp.manager import DETManager


class Configuracao_DET(models.Model):
    """Classe para models de configuração DETs"""

    tipo_registro = models.CharField(max_length=1)
    formato = models.CharField(max_length=6)
    cod_entidade = models.CharField(max_length=3)
    entidade = models.CharField(max_length=40)
    autuador = models.CharField(max_length=6)
    tipo_arquivo = models.CharField(max_length=1)
    cod_municipio = models.CharField(max_length=4, default='8179')
    filler = models.IntegerField()

    def __unicode__(self):
        return self.tipo_registro

    class Meta:
        app_label = "detransapp"


class DET(models.Model):
    """Classe para models de DETs"""

    codigo = models.CharField(max_length=255)

    objects = DETManager()

    def __unicode__(self):
        return self.codigo

    class Meta:
        app_label = "detransapp"
