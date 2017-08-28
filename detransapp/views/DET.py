# -*- coding:utf-8 -*-
"""Arquivo para mexer nas DETS"""
import os
import zipfile
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.DET import FormDet
from detransapp.models import Infracao, DET
from detransapp.models.DET import Configuracao_DET, DET
from detransapp.decorators import validar_imei, permissao_geral_required, autenticado
from detransapp.rest import JSONResponse


class CadastroDETView(View):
    template = 'det/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, det_id=None):

        det = Configuracao_DET.objects.filter()
        if len(det) > 0:
            det_id = det[0].id

        if det_id:
            det = Configuracao_DET.objects.get(pk=det_id)
            form = FormDet(instance=det)
        else:
            form = FormDet()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, det_id=None):

        det = Configuracao_DET.objects.filter()
        if len(det) > 0:
            det_id = det[0].id

        if det_id:
            cor = Configuracao_DET.objects.get(pk=det_id)
            form = FormDet(instance=cor, data=request.POST)

        else:

            form = FormDet(request.POST)

        if form.is_valid():
            form.save(request)

            return redirect('/')

        else:
            return redirect('/config/set/det')


class ConsultaDETView(View):
    template_name = 'det/consulta.html'

    @method_decorator(autenticado())
    def __page(self, request):
        procurar = ''

        if request.method == 'POST':

            if 'procurar' in request.POST:
                procurar = request.POST['procurar']

        else:

            if 'procurar' in request.GET:
                procurar = request.GET['procurar']

        try:
            page = int(request.GET.get('page', 1))
        except Exception:
            page = 1

        det_page = DET.objects.get_page(page, procurar)

        return render(request, self.template_name,
                      {'dets': det_page, 'procurar': procurar, 'formato': 0, 'formato1': 1})

    @method_decorator(autenticado())
    def get(self, request):
        return self.__page(request)

    def post(self, request):
        return self.__page(request)


class TemplateDET(View):
    template_name = 'det/template.html'

    @method_decorator(autenticado())
    def get(self, request):
        return render(request, self.template_name, )


class GeraDet(View):
    template_name = 'det/gera.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, filtro='0', formato=''):

        det = datetime.now().strftime("%Y%m%d%H%M%S")
        config = Configuracao_DET.objects.filter().order_by('-id')[0]
        nome_det = str(request).split('/')[3]
        if nome_det != "format":
            id_det = DET.objects.get(codigo=nome_det)
            sequencial_arquivo = str(id_det.id)
        else:
            sequencial_arquivo = str(len(DET.objects.all()) + 1)

        print ("det", DET.objects.all())

        while len(sequencial_arquivo) < 6:
            sequencial_arquivo = '0' + sequencial_arquivo

        autuador = ('0' * (6 - len(config.autuador))) + config.autuador

        nome_arq = config.formato + '.' + config.cod_entidade + '.' + \
                   autuador + '.' + sequencial_arquivo + '.DET'
        arq = open(nome_arq, 'w')

        if formato == '1':
            zp = zipfile.ZipFile(nome_arq[:len(nome_arq) - 4] + '.zip', 'w')

        if filtro == '0':
            det_novo = DET(codigo=det)
            det_novo.save()

        # topo

        if config:

            hoje = datetime.now()

            filler_entidade = len(config.entidade)
            entidade = config.entidade
            if filler_entidade < 40:
                qtd = 40 - filler_entidade
                # entidade = config.entidade.ljust(qt)
                entidade = config.entidade + (' ' * qtd)

            data = hoje.strftime('%Y%m%d')

            hora = hoje.strftime('%H%M')

            filler = (182 * ' ')

            registro_inicial = (5 * '0') + '1'

            cod_entidade = (str(config.cod_entidade))

            while len(cod_entidade) < 3:
                cod_entidade = '0' + cod_entidade

            topo = '0' + config.formato + cod_entidade + entidade + data + hora + str(
                sequencial_arquivo) + autuador + config.tipo_arquivo + \
                   filler + str(registro_inicial)
            arq.write(topo + '\r\n')

            # infracoes
            infracoes = Infracao.objects.filter(det=filtro, veiculo_id__isnull=False).distinct()
            # infracoes = Infracao.objects.filter(veiculo_id__isnull=False).distinct() # TESTE
            sequencial_registro = int(registro_inicial)

            for i in infracoes:

                # Registro de infracoes
                sequencial_registro = int(sequencial_registro) + 1
                if len(str(sequencial_registro)) < 6:
                    sequencial_registro = ('0' * (6 - len(str(sequencial_registro)))) \
                                          + str(sequencial_registro)

                tipo_registro = config.tipo_registro
                n_auto = str(i.id)
                if len(n_auto) < 10:
                    n_auto = ('0' * (10 - len(n_auto))) + n_auto
                local = i.local
                if len(local) < 80:
                    local = local.rstrip()
                    local = local + (' ' * (80 - len(local)))

                cod_municipio = config.cod_municipio

                tipo_inf = str(i.tipo_infracao_id)
                if tipo_inf == '':
                    cod_tipo_inf = '0' * 4
                    desmembramento = '0'

                if len(tipo_inf.split('-')) > 1:

                    cod_tipo_inf = ''
                    for y in range(len(tipo_inf.split('-'))):
                        cod_tipo_inf += tipo_inf.split('-')[y]
                    cod_tipo_inf = cod_tipo_inf[:4]
                    desmembramento = cod_tipo_inf[-1]

                condutor = '0'
                cnh = '0' * 11

                complemento = ' ' * 80
                if i.is_condutor_identi:
                    condutor = '1'
                    cnh = i.infrator.cnh.split('/')
                    cnh = cnh[0]
                    if len(cnh) == 0:
                        condutor = '3'

                    if len(cnh) < 11:
                        cnh = '0' * (11 - len(cnh)) + cnh

                filler = ' ' * 31
                infracao = tipo_registro + n_auto + i.veiculo.placa + i.veiculo.cidade.uf.sigla +\
                           i.data_infracao.strftime(
                         '%Y%m%d') + i.data_infracao.strftime(
                         '%H%M%S') + local + cod_municipio + cod_tipo_inf + desmembramento + \
                            condutor + cnh + i.agente.cpf + complemento + filler + str(
                             sequencial_registro)

                arq.write(infracao.encode('UTF-8') + '\r\n')
                if i.det == '0':
                    i.det = det
                    i.save()

            if len(str(qtd)) < 6:
                qtd = ('0' * (6 - qtd)) + str(qtd)

            # trailler
            sequencial_infracao = int(sequencial_registro) - 1
            if len(str(sequencial_infracao)) < 6:
                sequencial_infracao = ('0' * (6 - len(str(sequencial_infracao)))) + str(sequencial_infracao)

            sequencial_registro = int(sequencial_registro) + 1

            if len(str(sequencial_registro)) < 6:
                sequencial_registro = ('0' * (6 - len(str(sequencial_registro)))) + str(sequencial_registro)

            trailler = '9' + str(sequencial_infracao) + (' ' * 250) + str(sequencial_registro)

            arq.write(trailler + '\r\n')

            arq.close()
            # zipfile
            if formato == '1':
                zp.write(nome_arq)
                zp.close()
                os.remove(nome_arq)
                nome_arq = nome_arq[:len(nome_arq) - 4] + '.zip'

            down = open(nome_arq, 'r')
            response = HttpResponse(down, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % nome_arq
            os.remove(nome_arq)
            return response
        else:
            return redirect('/config/get/det')


class GetAutuadorRestView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self):
        det = Configuracao_DET.objects.filter()
        autuador = str(det[0].autuador)

        return JSONResponse({'autuador': autuador})
