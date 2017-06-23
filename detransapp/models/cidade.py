"""Model de cidade"""

from django.db import models
from detransapp.models.uf import UF
from detransapp.manager import CidadeManager


class Cidade(models.Model):
    """Classe para model de cidades"""

    codigo = models.IntegerField(primary_key=True)
    uf = models.ForeignKey(UF)
    nome = models.CharField(max_length=40)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)

    objects = CidadeManager()

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = "detransapp"
