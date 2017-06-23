"""Model para modelos"""

from django.db import models
from detransapp.manager import ModeloManager


class Modelo(models.Model):
    """Classe para model de modelos"""

    codigo = models.PositiveIntegerField(primary_key=True)
    descricao = models.CharField(max_length=40)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)
    objects = ModeloManager()

    def __unicode__(self):
        return self.descricao

    class Meta:
        app_label = "detransapp"
