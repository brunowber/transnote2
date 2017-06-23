# coding: utf-8
"""Gerencia as sincronizações de configuração"""

from datetime import datetime
from django.db import models


class ConfigSincManager(models.Manager):
    """Classe para gerenciar as configurações"""

    def get_config_sinc_sicronismo(self, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            query = self.filter(data_alterado__gt=data)
            return query.first()
        return self.first()
