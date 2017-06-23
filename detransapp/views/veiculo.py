# coding: utf-8
"""CRUD para veiculos"""

import chardet
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.veiculo import FormVeiculo, FormEditarVeiculo
from detransapp.models import Veiculo
from detransapp.serializers import VeiculoSerializer
from detransapp.rest import JSONResponse
from detransapp.forms.importacao import FormArquivo
from detransapp.decorators import validar_imei, permissao_geral_required


class CadastroVeiculoView(View):
    template = 'veiculo/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, veiculo_id=None):
        if veiculo_id:
            veiculo = Veiculo.objects.get(renavam=veiculo_id)

            form = FormVeiculo(veiculo.cidade.uf_id, instance=veiculo)
            form.fields['uf'].initial = veiculo.cidade.uf_id
        else:

            form = FormVeiculo(None)

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, veiculo_id=None):

        if veiculo_id:
            veiculo = Veiculo.objects.get(renavam=veiculo_id)
            form = FormEditarVeiculo(request.POST['uf'], data=request.POST, instance=veiculo)
        else:
            form = FormVeiculo(request.POST['uf'], request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaVeiculoView(View):
    template_name = 'veiculo/consulta.html'

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

        veiculos_page = Veiculo.objects.get_page(page, procurar)

        return render(request, self.template_name, {'veiculos': veiculos_page,
                                                    'procurar': procurar})

    def get(self, request):
        return self.__page(request)

    def post(self, request):
        print (request.POST)
        return self.__page(request)


class GetVeiculosRestView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):

        page = None
        if 'page' in request.POST:
            page = request.POST['page']
        if 'data' in request.POST:
            veiculos = Veiculo.objects.get_veiculos_sicronismo(page, request.POST['data'])
        else:
            veiculos = Veiculo.objects.get_veiculos_sicronismo(page)
        veiculos_js = []
        for veiculo in veiculos:
            serializer = VeiculoSerializer(veiculo)
            veiculos_js.append(serializer.data)
        page = {'num_pages': veiculos.paginator.num_pages,
                'number': veiculos.number, 'veiculos': veiculos_js}
        return JSONResponse(page)


class ImportaVeiculo(View):
    template_name = 'veiculo/importa.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        form = FormArquivo()

        return render(request, self.template_name, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        i = 0

        linhas_erro_encoding = []
        if 'arquivo' in request.FILES and str(request.FILES['arquivo'])[-4:] == ".txt":
            arq = request.FILES['arquivo']
            for linha in arq:
                if linha.strip() == '':
                    continue

                encoding = chardet.detect(linha)

                try:
                    linha = linha.encode('utf-8')
                except Exception:
                    linhas_erro_encoding.append((linha, encoding['encoding'],))
                    continue
                Veiculo.objects.importa_renavam(linha)
                i += 1

            return render(request, self.template_name, {'qtd': i, 'envio': True})
        else:
            form = FormArquivo()
            return render(request, self.template_name, {'form': form, 'erro': 'erro'})

'''
import chardet
class ImportaVeiculo(View):

    template_name = 'categoria/importa.html'

    def get(self, request):

        arq = open('detrans_txt/Renavam.txt', 'r')
        i = 0
        qtd = 0

        linhas_erro_encoding = []

        for linha in arq:

            if linha.strip() == '':
                continue

            encoding = chardet.detect(linha)

            try:
                linha = linha.encode('utf-8')
            except:
                linhas_erro_encoding.append((linha, encoding['encoding'],))
                continue

            #####placa = linha[0:7]
            modelo = linha[7:13]
            mod = Modelo.objects.get(codigo = modelo)
            cor = linha[13:15]
            cor = Cor.objects.get(codigo = cor)
            tipo_veiculo = linha[15:17]
            tp = TipoVeiculo.objects.get(codigo = tipo_veiculo)
            especie = linha[17:19]
            especie = Especie.objects.get(codigo=especie)
            categoria = linha[19:21]
            cat = Categoria.objects.get(codigo=categoria)
            municipio = linha[21:26]
            munic = Cidade.objects.get(codigo=municipio)
            renavam = linha[26:37].strip()
            anof = linha[37:41]
            anom = linha[41:45]
            cpf = linha[45:59].strip()
            nome = linha[59:119].strip()
            passageiros = linha[119:122]

            p = Proprietario(nome=nome, cpf=cpf)
            p.save()
            v = Veiculo(placa=placa,
                        modelo=mod, cor = cor, tipo_veiculo = tp, especie=especie, categoria = cat,
                        renavam= renavam, ano_fabricacao = anof,
                        ano_modelo = anom, num_passageiro=passageiros,
                        proprietario=p, cidade=munic)
            v.save()

            del p

            del v#####
            Veiculo.objects.importa_renavam(linha)
            qtd +=1
        print(qtd)

        return render(request, self.template_name, {'qtd': i, 'erros':linhas_erro_encoding})'''
