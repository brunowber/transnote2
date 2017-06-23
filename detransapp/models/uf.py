"""Model para UFs"""

from django.db import models

from detransapp.manager import UFManager


class UF(models.Model):
    """Classe para model de UFs"""

    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)
    objects = UFManager()

    def __unicode__(self):
        return self.sigla

    class Meta:
        app_label = "detransapp"
