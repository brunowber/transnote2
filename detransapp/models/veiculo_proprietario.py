"""Model para proprietarios de veiculos"""

from django.db import models
from detransapp.models.veiculo import Veiculo
from detransapp.models.proprietario import Proprietario


class VeiculoProprietario(models.Model):
    """Classe para models de proprietarios de veiculos"""

    veiculo = models.ForeignKey(Veiculo)
    proprietario = models.ForeignKey(Proprietario)
    data = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        app_label = "detransapp"
