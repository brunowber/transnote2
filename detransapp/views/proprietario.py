# coding: utf-8
"""CRUD de proprietario"""
from django.shortcuts import render, redirect
from django.views.generic.base import View
from detransapp.forms.proprietario import FormProprietario
from detransapp.models import Proprietario
from django.utils.decorators import method_decorator
from detransapp.decorators import permissao_geral_required, autenticado


class CadastroProprietarioView(View):
    template = 'proprietario/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, proprietario_id=None):

        if proprietario_id:
            proprietario = Proprietario.objects.get(pk=proprietario_id)
            form = FormProprietario(instance=proprietario)
        else:
            form = FormProprietario()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, proprietario_id=None):

        if proprietario_id:
            proprietario = Proprietario.objects.get(pk=proprietario_id)
            form = FormProprietario(instance=proprietario, data=request.POST)
        else:

            form = FormProprietario(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaProprietarioView(View):
    template_name = 'proprietario/consulta.html'

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

        proprietarios_page = Proprietario.objects.get_page(page, procurar)

        return render(request, self.template_name, {'proprietarios': proprietarios_page,
                                                    'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):

        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):

        return self.__page(request)
