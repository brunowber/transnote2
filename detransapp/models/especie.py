"""Model para especies"""

from django.db import models
from detransapp.manager import EspecieManager


class Especie(models.Model):
    """Classe para model de especies"""

    codigo = models.PositiveIntegerField(primary_key=True)
    descricao = models.CharField(max_length=40)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)
    objects = EspecieManager()

    def __unicode__(self):
        return self.descricao

    class Meta:
        app_label = "detransapp"
