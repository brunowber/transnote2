"""Model para dispositivos sem permissao"""

from django.db import models
from detransapp.manager import DispositivoManager


class Acesso(models.Model):
    """Classe para model de dispositivos sem permissao"""

    imei = models.CharField(max_length=17, unique=True)

    objects = DispositivoManager()

    def __unicode__(self):
        return self.imei

    class Meta:
        app_label = "detransapp"
