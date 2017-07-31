"""Gerencia os infratores"""

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class InfratorManager(models.Manager):
    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            condutores = self.filter(Q(nome__icontains=procurar) |
                                     Q(cnh__icontains=procurar) |
                                     Q(cpf__icontains=procurar) |
                                     Q(rg__icontains=procurar))
        else:
            condutores = self.filter()

        condutores = condutores.order_by('nome')

        paginator = Paginator(condutores, settings.NR_REGISTROS_PAGINA)
        try:
            condutores_page = paginator.page(page)
        except:
            condutores_page = paginator.page(paginator.num_pages)

        return condutores_page
