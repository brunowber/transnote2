# coding: utf-8
"""Gerencia as sincronizações de configuração"""

from datetime import datetime
from django.db import models


class DadosSqliteManager(models.Manager):
    """Classe para gerenciar as configurações"""

    def get_dados_sqlite_sicronismo(self, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            query = self.filter(is_finished=True)
            return query.all().order_by('-id')[:1]
        return self.first()
