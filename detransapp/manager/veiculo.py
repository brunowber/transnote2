# coding: utf-8
"""Gerencia os veiculos"""

from datetime import datetime
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from django.db import connection


class VeiculoManager(models.Manager):
    """Classe para gerenciar os veiculos"""

    def get_page(self, page, procurar):

        if procurar is not None and procurar != '':
            veiculos = self.filter(Q(placa__icontains=procurar) |
                                   Q(modelo__descricao__icontains=procurar))
        else:
            veiculos = self.filter()

        veiculos = veiculos.order_by('placa')

        paginator = Paginator(veiculos, settings.NR_REGISTROS_PAGINA)
        try:
            veiculos_page = paginator.page(page)
        except:
            veiculos_page = paginator.page(paginator.num_pages)

        return veiculos_page

    def get_veiculos_sicronismo(self, page, data=None):
        try:
            if data:
                data = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')
                veiculos = self.filter(data_alterado__gt=data)
            else:
                veiculos = self.filter()
        except Exception:
            print "Falha no servidor "

        veiculos = veiculos.order_by('renavam')

        paginator = Paginator(veiculos, 100000)

        if page:
            veiculos_page = paginator.page(page)

        else:
            veiculos_page = paginator.page(1)
        return veiculos_page

    @staticmethod
    def importa_renavam(linha):
        placa_veiculo = linha[0:7]
        modelo_veiculo = int(linha[7:13])
        cor_veiculo = int(linha[13:15])
        tipo_veiculo = int(linha[15:17])
        especie_veiculo = int(linha[17:19])
        categoria_veiculo = int(linha[19:21])
        municipio_veiculo = linha[21:26]
        renavam_veiculo = linha[26:37].strip()
        ano_fabricacao_veiculo = linha[37:41]
        ano_modelo_veiculo = linha[41:45]
        cpf_proprietario = linha[45:59].strip()
        nome_proprietario = linha[59:119].strip()
        num_passageiros_veiculo = linha[119:122]
        chassi_veiculo = linha[122:143].strip()
        nr_motor_veiculo = linha[143:164].strip()

        cur = connection.cursor()
        cur.callproc('insert_renavam', [nome_proprietario,
                                        cpf_proprietario,
                                        modelo_veiculo,
                                        cor_veiculo,
                                        tipo_veiculo,
                                        especie_veiculo,
                                        categoria_veiculo,
                                        municipio_veiculo,
                                        placa_veiculo,
                                        renavam_veiculo,
                                        num_passageiros_veiculo,
                                        ano_fabricacao_veiculo,
                                        ano_modelo_veiculo,
                                        chassi_veiculo,
                                        nr_motor_veiculo])

        cur.close()
