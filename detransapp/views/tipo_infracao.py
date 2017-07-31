# coding: utf-8
"""CRUD para tipos de infração"""
import os

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.tipo_infracao import FormTipoInfracao
from detransapp.models import TipoInfracao
from detransapp.models import Lei
from detransapp.serializers import TipoInfracaoSerializer
from detransapp.rest import JSONResponse
from detransapp.decorators import validar_imei, permissao_geral_required


class CadastroTipoInfracaoView(View):
    template = 'tipo_infracao/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, tipo_infracao_id=None):

        if tipo_infracao_id:
            tipo_infracao = TipoInfracao.objects.get(pk=tipo_infracao_id)

            form = FormTipoInfracao(instance=tipo_infracao)

        else:

            form = FormTipoInfracao()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, tipo_infracao_id=None):

        if tipo_infracao_id:
            tipo_infracao = TipoInfracao.objects.get(pk=tipo_infracao_id)
            form = FormTipoInfracao(request.POST, instance=tipo_infracao)

        else:

            form = FormTipoInfracao(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaTipoInfracaoView(View):

    template_name = 'tipo_infracao/consulta.html'

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

        tipos_page = TipoInfracao.objects.get_page(page, procurar)

        return render(request, self.template_name, {'tipos': tipos_page, 'procurar': procurar})

    def get(self, request):

        return self.__page(request)

    def post(self, request):

        return self.__page(request)


class GetTiposInfracaoRestView(APIView):
    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        page = None

        if 'page' in request.POST:
            page = request.POST['page']

        if 'data' in request.POST:
            tipos_infracao = TipoInfracao.objects.get_tipos_infracao_sicronismo(
                page, request.POST['data'])
        else:
            tipos_infracao = TipoInfracao.objects.get_tipos_infracao_sicronismo(page)
        tipos_infracao_js = []

        for tipo_infracao in tipos_infracao:
            serializer = TipoInfracaoSerializer(tipo_infracao)
            tipos_infracao_js.append(serializer.data)

        page = {'num_pages': tipos_infracao.paginator.num_pages, 'number': tipos_infracao.number,
                'tipos_infracao': tipos_infracao_js}

        return JSONResponse(page)


class CarregaTiposInfracao(View):
    template = 'tipo_veiculo/carregatipos.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        module_dir = os.path.dirname(__file__)  # get current directory
        path = os.path.join(module_dir, 'tipos2.csv')
        abrir = open(path, 'r')

        for line in abrir:
            l = line.split(',')
            ls = Lei.objects.filter(lei=l[1])
            if ls:
                lei = ls[0]
            else:
                lei = Lei(lei=l[1])
                lei.save()
            t = TipoInfracao(codigo=l[0].strip(), descricao=l[2].strip(), lei=lei)
            t.save()
        abrir.close()

        tipos = TipoInfracao.objects.all()
        return render(request, self.template, {'tipos': tipos})
