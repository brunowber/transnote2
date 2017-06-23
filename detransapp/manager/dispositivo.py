"""Gerencia os dispositivos"""

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class DispositivoManager(models.Manager):
    """Classe para gerenciar os dispositivos"""

    def existe_dispositivo(self, imei):

        return self.filter(imei=imei, ativo=True).first() is not None

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            dispostivos = self.filter(Q(imei__icontains=procurar))
        else:
            dispostivos = self.filter()

        dispostivos = dispostivos.order_by('-ativo')
        return dispostivos
        paginator = Paginator(dispostivos, settings.NR_REGISTROS_PAGINA)
        try:
            dispostivos_page = paginator.page(page)
        except:
            dispostivos_page = paginator.page(paginator.num_pages)

        return dispostivos_page
