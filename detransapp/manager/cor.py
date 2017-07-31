# coding: utf-8
"""Gerencia as cores"""

from datetime import datetime
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class CorManager(models.Manager):
    """Classe para gerenciar as cores"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            cores = self.filter(Q(descricao__icontains=procurar))
        else:
            cores = self.filter()

        cores = cores.order_by('descricao')

        paginator = Paginator(cores, settings.NR_REGISTROS_PAGINA)
        try:
            blocos_page = paginator.page(page)
        except:
            blocos_page = paginator.page(paginator.num_pages)

        return blocos_page

    def get_cores_sicronismo(self, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            query = self.filter(data_alterado__gt=data)
            return query.all()
        return self.all()
