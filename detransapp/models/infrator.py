"""Models para infratores"""

from django.db import models
from detransapp.models.pessoa import Pessoa


class Infrator(Pessoa):
    """Classe para models de infratores"""

    estado = models.CharField(max_length=255, null=True)
    cidade = models.CharField(max_length=255, null=True)
    endereco = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = "detransapp"
