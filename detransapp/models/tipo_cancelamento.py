"""Model para os tipos de cancelamento"""

from django.db import models

from detransapp.manager import TipoCancelamentoManager


class TipoCancelamento(models.Model):
    """Classe para os tipos de cancelamento"""

    codigo = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=100)

    objects = TipoCancelamentoManager()

    def __unicode__(self):
        return str(self.codigo)

    class Meta:
        app_label = "detransapp"
