"""Model para pessoas"""

from django.db import models


class Pessoa(models.Model):
    """Classe para model de pessoas"""

    documento = models.CharField(db_index=True, max_length=25, primary_key=True)
    nome = models.CharField(max_length=60)

    cnh = models.CharField(max_length=30, null=True)

    def __eq__(self, other):
        if other:
            return self.documento == other.documento and self.nome == other.nome
        return False

    class Meta:
        abstract = True
