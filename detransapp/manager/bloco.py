"""Gerenciador de blocos"""
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class BlocoManager(models.Manager):
    """Classe para gerenciar os blocos"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            blocos = self.filter(Q(inicio_intervalo__icontains=procurar))
        else:
            blocos = self.filter()

        blocos = blocos.order_by('inicio_intervalo')

        paginator = Paginator(blocos, settings.NR_REGISTROS_PAGINA)
        try:
            blocos_page = paginator.page(page)
        except Exception:
            blocos_page = paginator.page(paginator.num_pages)

        return blocos_page
