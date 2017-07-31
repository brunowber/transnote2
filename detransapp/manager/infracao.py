# coding: utf-8
"""Gerencia as infrações"""

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings


class InfracaoManager(models.Manager):
    """Classe para gerenciar as infrações"""

    def get_page(self, page, procurar):
        if procurar.isdigit():
            infracoes = self.filter(Q(data_infracao__hour=procurar) |
                                    Q(veiculo__placa__icontains=procurar))
        elif procurar is not None and procurar != '':
            infracoes = self.filter(Q(obs__icontains=procurar) |
                                    Q(local__icontains=procurar) |
                                    Q(veiculo__placa__icontains=procurar) |
                                    Q(is_cancelado__icontains=procurar) |
                                    Q(agente__first_name__icontains=procurar))
        else:
            infracoes = self.filter()
        infracoes = infracoes.order_by('-id')

        paginator = Paginator(infracoes, settings.NR_REGISTROS_PAGINA)
        try:
            infracoes_page = paginator.page(page)
        except:
            infracoes_page = paginator.page(paginator.num_pages)
        return infracoes_page

        # def get_marcas_sicronismo(self, data=None):
        #	 if data:
        #		 data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
        #		 query = self.filter(data_alterado__gt=data)
        #		 return query.all()
        #	 return self.all()
