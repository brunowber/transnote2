"""Model para categorias"""

from django.db import models
from detransapp.manager import CategoriaManager


class Categoria(models.Model):
    """Classe para model de categoria"""

    codigo = models.PositiveIntegerField(primary_key=True)
    descricao = models.CharField(max_length=40)
    data = models.DateTimeField(auto_now_add=True)
    data_alterado = models.DateTimeField(auto_now=True)

    objects = CategoriaManager()

    def __unicode__(self):
        return self.descricao

    class Meta:
        app_label = "detransapp"
