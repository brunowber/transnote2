"""Model para veiculos estrangeiros"""

from django.db import models
from detransapp.models.infracao import Infracao


class VeiculoEstrangeiro(models.Model):
    """Classe para models de veiculos estrangeiros"""

    infracao = models.ForeignKey(Infracao)
    pais = models.CharField(null=True, max_length=50)
    modelo = models.CharField(null=True, max_length=50)
    especie = models.CharField(null=True, max_length=50)
    placa = models.CharField(max_length=20, null=True)
    chassi = models.CharField(null=True, max_length=50)
    nr_motor = models.CharField(max_length=50, null=True)
    tipo_veiculo = models.CharField(max_length=40, null=True)
    cor = models.CharField(max_length=40, null=True)
    categoria = models.CharField(max_length=40, null=True)
    ano_fabricacao = models.IntegerField(null=True)
    ano_modelo = models.IntegerField(null=True)
    num_passageiro = models.CharField(max_length=3, null=True)

    def __unicode__(self):
        return self.chassi

    class Meta:
        app_label = "detransapp"
