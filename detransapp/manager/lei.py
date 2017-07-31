# coding: utf-8
"""Gerencia as leis"""

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class LeiManager(models.Manager):
    """Classe para gerenciar as leis"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            leis = self.filter(Q(lei__icontains=procurar))
        else:
            leis = self.filter()

        leis = leis.order_by('lei')

        paginator = Paginator(leis, settings.NR_REGISTROS_PAGINA)
        try:
            leis_page = paginator.page(page)
        except Exception:
            leis_page = paginator.page(paginator.num_pages)

        return leis_page
