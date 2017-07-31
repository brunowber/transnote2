# coding: utf-8
"""Gerencia as regiões"""

from datetime import datetime
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class RegiaoManager(models.Manager):
    """Classe para gerenciar as regiões"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            regioes = self.filter(Q(sigla__icontains=procurar) | Q(nome__icontains=procurar))
        else:
            regioes = self.filter()

        regioes = regioes.order_by('sigla')

        paginator = Paginator(regioes, settings.NR_REGISTROS_PAGINA)
        try:
            regioes_page = paginator.page(page)
        except Exception:
            regioes_page = paginator.page(paginator.num_pages)

        return regioes_page

    def get_regioes_sicronismo(self, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            query = self.filter(data_alterado__gt=data)
            return query.all()
        return self.all()
