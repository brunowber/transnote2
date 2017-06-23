# coding: utf-8
"""Gerencia os tipos de infração"""

from datetime import datetime
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class TipoInfracaoManager(models.Manager):
    """Classe para gerenciar os tipos de infração"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            tipos = self.filter(Q(descricao__icontains=procurar))
        else:
            tipos = self.filter()

        tipos = tipos.order_by('descricao')

        paginator = Paginator(tipos, settings.NR_REGISTROS_PAGINA)
        try:
            tipos_page = paginator.page(page)
        except Exception:
            tipos_page = paginator.page(paginator.num_pages)

        return tipos_page

    def get_tipos_infracao_sicronismo(self, page, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            tipos_infracao = self.filter(data_alterado__gt=data)

        else:
            tipos_infracao = self.filter()

        paginator = Paginator(tipos_infracao, 5000)

        if page:
            tipos_infracao_page = paginator.page(page)
        else:
            tipos_infracao_page = paginator.page(1)

        return tipos_infracao_page
