# coding: utf-8
"""Cadastra e atualiza as categorias"""

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.forms.categoria import FormCategoria
from detransapp.models import Categoria
from detransapp.forms.importacao import FormArquivo
from detransapp.decorators import permissao_geral_required
from detransapp.rest import JSONResponse
from detransapp.serializers import CategoriaSerializer


class CadastroCategoriaView(View):
    """Cadastra as categorias"""

    template = 'categoria/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, categoria_id=None):
        """Pega o formulário para cadastrar e atualizar uma categoria"""

        if categoria_id:
            categoria = Categoria.objects.get(pk=categoria_id)
            form = FormCategoria(instance=categoria)
        else:
            form = FormCategoria()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, categoria_id=None):
        """Envia para o servidor a nova categoria cadastrada ou atualizada"""

        if categoria_id:
            categoria = Categoria.objects.get(pk=categoria_id)
            form = FormCategoria(instance=categoria, data=request.POST)
        else:

            form = FormCategoria(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaCategoriaView(View):
    """retorna as categorias para consulta"""

    template_name = 'categoria/consulta.html'

    def __page(self, request):
        """Volta as páginas das categorias procuradas"""
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

        categorias_page = Categoria.objects.get_page(page, procurar)

        return render(request, self.template_name, {'categorias':
                                                        categorias_page, 'procurar': procurar})

    def get(self, request):
        """Volta a primeira página da consulta"""

        return self.__page(request)

    def post(self, request):
        """Volta as categorias pesquisadas"""

        return self.__page(request)


class GetCategoriasRestView(APIView):
    """Manda do servidor para o android as categórias"""

    permission_classes = (IsAuthenticated, AllowAny)

    def post(self, request):
        """Retorna as categorias nas infrações"""
        if 'data' in request.POST:
            categorias = Categoria.objects.get_categorias_sicronismo(request.POST['data'])
        else:
            categorias = Categoria.objects.get_categorias_sicronismo()

        cores_js = []
        for categoria in categorias:
            serializer = CategoriaSerializer(categoria)
            cores_js.append(serializer.data)
        return JSONResponse(cores_js)


class ImportaCategoria(View):
    """Importa as categorias"""

    template_name = 'categoria/importa.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        """Cria um formulário de categorias"""
        form = FormArquivo()

        return render(request, self.template_name, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        """Manda os arquivos importados para o servidor"""
        i = 0

        if 'arquivo' in request.FILES and str(request.FILES['arquivo'])[-4:] == ".txt":
            arq = request.FILES['arquivo']
            for linha in arq:
                try:
                    linha = linha.encode('UTF-8')

                    cod = linha[0:2]
                    desc = linha[2:].strip()
                    nova_categoria = Categoria(codigo=cod, descricao=desc)
                    nova_categoria.save()
                    i += 1
                except Exception:
                    pass

            return render(request, self.template_name, {'qtd': i, 'envio': True})
        else:
            form = FormArquivo()
            return render(request, self.template_name, {'form': form, 'erro': 'erro'})
