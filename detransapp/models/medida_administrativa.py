"""Model para medidas administrativas"""

from django.db import models


class MedidaAdminstrativa(models.Model):
    """Classe para model de medidas administrativas"""

    codigo = models.CharField(max_length=10)
    descricao = models.TextField(null=True)

    def __unicode__(self):
        return str(self.pk)
