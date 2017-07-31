"""Gerenciador de agentes"""
from datetime import datetime
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class AgenteManager(models.Manager):
    """Classe para gerenciar a procura de agentes"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            agentes = self.filter(Q(identificacao__icontains=procurar) |
                                  Q(first_name__icontains=procurar))
        else:
            agentes = self.filter()

        agentes = agentes.order_by('first_name')

        paginator = Paginator(agentes, settings.NR_REGISTROS_PAGINA)
        try:
            agentes_page = paginator.page(page)
        except:
            agentes_page = paginator.page(paginator.num_pages)

        return agentes_page

    def get_agentes_sicronismo(self, data=None):
        if data:
            data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
            query = self.filter(data_alterado__gt=data)
            return query.all()
        return self.all()
