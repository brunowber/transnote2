# -*- coding: utf-8 -*-
# from wkhtmltopdf.views import PDFTemplateResponse
# from pandas.tseries.frequencies import infer_freq
import base64
import sys
import traceback
from json import loads, dumps
from datetime import datetime
from django.http import HttpResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.models import Infracao, Image, Configuracao_DET
from detransapp.models import Infrator, Movimentacao, Dispositivo, \
    VeiculoEditado, VeiculoEstrangeiro
from detransapp.decorators import validar_imei


class RelatorioInfracaoDetalhesView(View):
    template = 'infracao/detalhes.html'

    def get(self, request, infracao_id=None):

        vei = ''
        if infracao_id:
            try:
                inf = Infracao.objects.get(pk=infracao_id)
                img = Image.objects.filter(infracao=infracao_id)
                det = Configuracao_DET.objects.filter()[0]
                if inf.is_estrangeiro:
                    vei = VeiculoEstrangeiro.objects.get(infracao=infracao_id)
                if inf.is_veiculo_editado:
                    vei = VeiculoEditado.objects.get(infracao=infracao_id)
                return render(request, self.template, {'infracao': inf, 'imagens': img,
                                                       'det': det, 'vei': vei})
            except Exception:
                return redirect('/infracao/relatorio/')
        else:
            return render(request, self.template)


class RelatorioInfracaoView(View):
    template = 'infracao/relatorio.html'

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

        infracao_page = Infracao.objects.get_page(page, procurar)
        return render(request, self.template, {'infracoes': infracao_page, 'procurar': procurar})

    def get(self, request):

        return self.__page(request)

    def post(self, request):

        return self.__page(request)


class RecebeInfracoesRestView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):

        infracoes_sinc = []
        infracoes_json = loads(request.POST['infracoes'])

        for inf_json in infracoes_json:

            sid = transaction.savepoint()
            try:
                is_estrangeiro = True
                if inf_json['is_estrangeiro'] == '0':
                    is_estrangeiro = False

                is_editado = True

                if inf_json['is_editado'] == '0':
                    is_editado = False

                is_condutor_identificado = True

                if inf_json['is_condutor_identificado'] == '0':
                    is_condutor_identificado = False

                infracao = Infracao()

                if inf_json['is_cancelado'] == "1":
                    infracao.is_cancelado = False
                else:
                    infracao.is_cancelado = True
                    infracao.motivo_cancelamento = inf_json['motivo_cancelamento']
                    infracao.data_cancelamento = datetime.strptime(inf_json['data'],
                                                                   "%d/%m/%Y %H:%M:%S")

                infracao.agente_id = request.user.id

                infracao.dispositivo_id = Dispositivo.objects.get(
                    imei=request.POST['imei']).id

                infracao.id = int(inf_json['infracao_id'])
                infracao.data_infracao = datetime.strptime(inf_json['data'], "%d/%m/%Y %H:%M:%S")
                infracao.local = inf_json['local']

                infracao.local_numero = inf_json['local_numero']
                if inf_json['observacao'] != '':
                    infracao.obs = inf_json['observacao']

                if inf_json['veiculo_id'] != "null":
                    infracao.veiculo_id = inf_json['veiculo_id']

                infracao.tipo_infracao_id = inf_json['tipo_infracao_id']
                if inf_json['tipo_infracao_id'] == 'null':
                    infracao.tipo_infracao_id = None

                movimentacao = Movimentacao()
                movimentacao.tempo = datetime.strptime(inf_json['data'], "%d/%m/%Y %H:%M:%S")
                movimentacao.latitude = inf_json['latitude']
                movimentacao.longitude = inf_json['longitude']
                movimentacao.save()

                infracao.movimento_id = movimentacao.id

                if inf_json['is_cancelado'] == "0":
                    infracao.is_cancelado = True
                    infracao.data_cancelamento = datetime.strptime(inf_json['data'],
                                                                   "%d/%m/%Y %H:%M:%S")
                    infracao.motivo_cancelamento = inf_json['motivo_cancelamento']

                if is_condutor_identificado:
                    verificar = Infrator.objects.filter(documento=inf_json['infrator']['documento'])
                    if len(verificar) == 0:
                        infrator = Infrator()
                        infrator.nome = inf_json['infrator']['nome']
                        infrator.cnh = inf_json['infrator']['cnh']
                        infrator.documento = inf_json['infrator']['documento']
                        infrator.save()
                        infracao.infrator_id = infrator.documento
                    else:
                        infracao.infrator_id = verificar[0].documento

                infracao.is_estrangeiro = is_estrangeiro
                infracao.is_condutor_identi = is_condutor_identificado
                infracao.is_veiculo_editado = is_editado

                if inf_json['data_ocorrencia'] == '':
                    infracao.data_ocorrencia = datetime.strptime(inf_json['data'],
                                                                 "%d/%m/%Y %H:%M:%S")
                else:
                    infracao.data_ocorrencia = datetime.strptime(inf_json['data_ocorrencia'],
                                                                 "%d/%m/%Y %H:%M:%S")
                infracao.status_cnh = inf_json['status_cnh']

                if not Infracao.objects.filter(id=infracao.id).exists():
                    infracao.save(force_insert=True)

                if is_editado:
                    veiculo_editado = VeiculoEditado()
                    if inf_json['veiculo_id'] == "null":
                        veiculo_editado.veiculo_id = None
                    else:
                        veiculo_editado.veiculo_id = inf_json['veiculo_id']
                    veiculo_editado.placa = inf_json['veiculo']['placa']
                    veiculo_editado.chassi = inf_json['veiculo']['chassi']
                    veiculo_editado.uf = inf_json['veiculo']['estado']
                    veiculo_editado.especie = inf_json['veiculo']['especie']
                    veiculo_editado.tipo_veiculo = inf_json['veiculo']['tipo_veiculo']
                    veiculo_editado.modelo = inf_json['veiculo']['modelo']
                    veiculo_editado.cor = inf_json['veiculo']['cor']
                    veiculo_editado.cidade = inf_json['veiculo']['cidade']
                    veiculo_editado.categoria = inf_json['veiculo']['categoria']
                    veiculo_editado.num_passageiro = inf_json['veiculo']['num_passageiros']

                    veiculo_editado.infracao_id = infracao.id
                    veiculo_editado.save()

                if is_estrangeiro:
                    veiculo_estrangeiro = VeiculoEstrangeiro()
                    veiculo_estrangeiro.pais = inf_json['veiculo']['pais']
                    veiculo_estrangeiro.modelo = inf_json['veiculo']['modelo']
                    veiculo_estrangeiro.especie = inf_json['veiculo']['especie']
                    veiculo_estrangeiro.placa = inf_json['veiculo']['placa']
                    veiculo_estrangeiro.chassi = inf_json['veiculo']['chassi']
                    veiculo_estrangeiro.tipo_veiculo = inf_json['veiculo']['tipo_veiculo']
                    veiculo_estrangeiro.cor = inf_json['veiculo']['cor']
                    veiculo_estrangeiro.categoria = inf_json['veiculo']['categoria']
                    # veiculo_estrangeiro.nr_motor = inf_json['veiculo']['nr_motor']
                    # veiculo_estrangeiro.ano_fabricacao = inf_json['veiculo']['ano_fabricacao']
                    # veiculo_estrangeiro.ano_modelo = inf_json['veiculo']['ano_modelo']
                    veiculo_estrangeiro.num_passageiro = inf_json['veiculo']['num_passageiros']
                    veiculo_estrangeiro.infracao_id = infracao.id
                    veiculo_estrangeiro.save()

                    # TODO VERIFICAR SE ESSES CAMPOS ESTÃO CORRETOS
                    '''
                    veiculo_estrangeiro.tipo_veiculo_id = inf_json['veiculo']['tipo_veiculo_id']
                    veiculo_estrangeiro.cor_id = inf_json['veiculo']['cor_id']
                    veiculo_estrangeiro.categoria_id = inf_json['veiculo']['categoria_id']
                    '''

                infracoes_sinc.append({'id': infracao.id, 'status': True})
                transaction.savepoint_commit(sid)

            except NameError:

                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)

        json = dumps(infracoes_sinc, ensure_ascii=False)
        return HttpResponse(json)


class GetImageRestView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)

    # @method_decorator(validar_imei())
    def post(self, request):

        ids_json = str(request.POST['id_infringement']).split(",")
        img_json = "" + str(request.POST['imagem'])
        img_json = img_json.split(",")

        status_core = []
        count = 0

        if len(ids_json) == 0:
            return NameError

        for ids in ids_json:
            if ids != '':
                Img = Image()
                print ids
                Img.infracao_id = int(ids)

                imgdata = base64.b64decode(img_json[count])
                filename = 'media/infracao_images/inf' + str(count) + str(Img.infracao_id) + '.png'

                with open(filename, 'wb') as f:
                    f.write(imgdata)

                Img.photo = filename
                Img.save()
                status_core.append({'id': ids, 'status': True})

                count += 1

        img_sinc = dumps(status_core, ensure_ascii=False)
        return HttpResponse(img_sinc)


class ServeImage(APIView):
    permission_classes = (IsAuthenticated, AllowAny)
    template = 'imagem/salvar.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        pass


class DET007(View):
    def gerar(self):
        infracoes = Infracao.objects.all()

        for i in infracoes:
            return i
