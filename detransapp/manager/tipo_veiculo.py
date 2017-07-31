# coding: utf-8
"""Gerencia os tipos de veiculos"""

from datetime import datetime
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class TipoVeiculoManager(models.Manager):
    """Classe pra gerenciar os tipos de veiculos"""

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

    def get_tipos_veiculo_sicronismo(self, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            query = self.filter(data_alterado__gt=data)
            return query.all()
        return self.all()
