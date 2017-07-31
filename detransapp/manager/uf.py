# coding: utf-8
"""Gerencia as UFs"""

from datetime import datetime
from django.db import models


class UFManager(models.Manager):
    """Classe para gerenciamento das UFs"""

    def get_ufs_sicronismo(self, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            query = self.filter(data_alterado__gt=data)
            return query.all()
        return self.all()
