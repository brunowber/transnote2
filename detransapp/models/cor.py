"""Model para cores"""

from django.db import models
from detransapp.manager import CorManager


class Cor(models.Model):
    """Classe para model de cores"""

    codigo = models.PositiveIntegerField(primary_key=True)
    descricao = models.CharField(max_length=40)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)

    objects = CorManager()

    def __unicode__(self):
        return self.descricao

    class Meta:
        app_label = "detransapp"
