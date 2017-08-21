# coding: utf-8
"""CRUD de modelo"""
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.models import Modelo
from detransapp.serializers import ModeloSerializer
from detransapp.rest import JSONResponse
from detransapp.forms.modelo import FormModelo
from detransapp.forms.importacao import FormArquivo
from detransapp.decorators import validar_imei, registro_log_sinc, permissao_geral_required, autenticado


class CadastroModeloView(View):
    template = 'modelo/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, modelo_id=None):

        if modelo_id:
            
            modelo = Modelo.objects.get(pk=modelo_id)
            form = FormModelo(instance=modelo)

        else:
            form = FormModelo()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, modelo_id=None):

        if modelo_id:
            
            modelo = Modelo.objects.get(pk=modelo_id)
            form = FormModelo(instance=modelo, data=request.POST)
        else:
            
            form = FormModelo(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaModeloView(View):
    template_name = 'modelo/consulta.html'

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

        modelos_page = Modelo.objects.get_page(page, procurar)

        return render(request, self.template_name, {'modelos': modelos_page, 'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):

        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):

        return self.__page(request)


class GetModelosRestView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    @method_decorator(registro_log_sinc(1))
    def post(self, request):
        page = None

        if 'page' in request.POST:
            page = request.POST['page']

        if 'data' in request.POST:

            modelos = Modelo.objects.get_modelos_sicronismo(page, request.POST['data'])
        else:
            modelos = Modelo.objects.get_modelos_sicronismo(page)
        modelos_js = []
        for modelo in modelos:
            serializer = ModeloSerializer(modelo)
            modelos_js.append(serializer.data)

        page = {'num_pages': modelos.paginator.num_pages,
                'number': modelos.number, 'modelos': modelos_js}

        return JSONResponse(page)


class ImportaModelo(View):
    template_name = 'modelo/importa.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        form = FormArquivo()

        return render(request, self.template_name, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        i = 0
        if 'arquivo' in request.FILES and str(request.FILES['arquivo'])[-4:] == ".txt":
            arq = request.FILES['arquivo']
            for linha in arq:
                try:
                    linha = linha.encode('UTF-8')
                    cod = linha[0:6]
                    desc = linha[6:].strip()
                    novo_modelo = Modelo(modelo_id=cod, descricao=desc)
                    novo_modelo.save()
                    i += 1
                except Exception:
                    continue
        else:
            form = FormArquivo()
            return render(request, self.template_name, {'form': form, 'erro': 'erro'})

        return render(request, self.template_name, {'qtd': i, 'envio': True})
