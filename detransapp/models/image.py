"""Model para imagens"""

from django.db import models
from detransapp.models.infracao import Infracao


class Image(models.Model):
    """Classe para model de imagens"""

    infracao = models.ForeignKey(Infracao)
    photo = models.ImageField(null=True)

    class Meta:
        app_label = "detransapp"
