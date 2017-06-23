# coding: utf-8
"""Gerencia os modelos"""

from datetime import datetime
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class ModeloManager(models.Manager):
    """Classe para gerenciar os modelos"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            modelos = self.filter(Q(descricao__icontains=procurar))
        else:
            modelos = self.filter()

        modelos = modelos.order_by('descricao')

        paginator = Paginator(modelos, settings.NR_REGISTROS_PAGINA)
        try:
            modelos_page = paginator.page(page)
        except Exception:
            modelos_page = paginator.page(paginator.num_pages)

        return modelos_page

    def get_modelos_sicronismo(self, page, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            modelos = self.filter(data_alterado__gt=data)

        else:
            modelos = self.filter()

        paginator = Paginator(modelos, 5000)

        if page:
            modelos_page = paginator.page(page)
        else:
            modelos_page = paginator.page(1)

        return modelos_page
