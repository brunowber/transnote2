"""Model para tipos de veiculos"""

from django.db import models
from detransapp.manager import TipoVeiculoManager


class TipoVeiculo(models.Model):
    """classe para model de tipos de veiculos"""

    codigo = models.PositiveIntegerField(primary_key=True)
    descricao = models.CharField(max_length=40)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)
    objects = TipoVeiculoManager()

    def __unicode__(self):
        return self.descricao

    class Meta:
        app_label = "detransapp"
