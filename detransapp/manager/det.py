# coding: utf-8
"""Gerencia as DETs"""

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class DETManager(models.Manager):
    """Classe para gerenciar as DETs"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            dets = self.filter(Q(codigo__icontains=procurar))
        else:
            dets = self.filter()

        dets = dets.order_by('codigo')

        paginator = Paginator(dets, settings.NR_REGISTROS_PAGINA)
        try:
            dets_page = paginator.page(page)
        except Exception:
            dets_page = paginator.page(paginator.num_pages)

        return dets_page
