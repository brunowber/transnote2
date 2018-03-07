#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Model para criação de banco móvel"""

from django.db import models
from detransapp.manager.dados_sqlite import DadosSqliteManager


class Detrans_sqlite(models.Model):
    """Classe para model de criação de banco móvel"""

    data_versao = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    objects = DadosSqliteManager()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        app_label = "detransapp"
