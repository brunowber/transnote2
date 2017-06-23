"""Model para o sistema"""

from django.db import models


class Sistema(models.Model):
    """Classe para a model do sistema"""

    sigla = models.CharField(max_length=150)
    nome_completo = models.CharField(max_length=150)
    logo = models.FileField(upload_to='images/')
    data = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.sigla

    class Meta:
        app_label = "detransapp"
