"""Model para veiculos editados"""

from django.db import models
from detransapp.models.infracao import Infracao
from detransapp.models.veiculo import Veiculo


class VeiculoEditado(models.Model):
    """Classe para models de veiculos editados"""

    infracao = models.ForeignKey(Infracao)
    veiculo = models.ForeignKey(Veiculo, null=True)
    chassi = models.CharField(null=True, max_length=21)
    renavam = models.BigIntegerField(null=True)
    nr_motor = models.CharField(max_length=21, null=True)
    placa = models.CharField(max_length=7)
    modelo = models.CharField(max_length=40, null=True)
    tipo_veiculo = models.CharField(max_length=40, null=True)
    especie = models.CharField(max_length=40, null=True)
    cidade = models.CharField(max_length=40, null=True)
    uf = models.CharField(max_length=40, null=True)
    cor = models.CharField(max_length=40, null=True)
    categoria = models.CharField(max_length=40, null=True)
    ano_fabricacao = models.IntegerField(null=True)
    ano_modelo = models.IntegerField(null=True)
    num_passageiro = models.CharField(max_length=3, null=True)

    def __unicode__(self):
        return self.chassi

    class Meta:
        app_label = "detransapp"
