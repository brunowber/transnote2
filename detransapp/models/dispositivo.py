"""Model para dispositivos"""

from django.db import models
from detransapp.manager import DispositivoManager


class Dispositivo(models.Model):
    """Classe para model de dispositivos"""

    imei = models.CharField(max_length=17, unique=True)

    ativo = models.BooleanField(default=True)

    objects = DispositivoManager()

    def __unicode__(self):
        return self.imei

    class Meta:
        app_label = "detransapp"
