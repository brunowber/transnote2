# coding: utf-8
"""Model para movimentação"""

from django.db import models


class Movimentacao(models.Model):
    """Classe para model de movimentação"""

    tempo = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        app_label = "detransapp"
