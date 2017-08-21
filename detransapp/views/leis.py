# coding: utf-8

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from detransapp.forms.lei import FormLei
from detransapp.models.lei import Lei
from detransapp.decorators import permissao_geral_required, autenticado



class CadastroLeisView(View):
    template = 'leis/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, condutor_id=None):

        if condutor_id:
            leis = Lei.objects.get(pk=condutor_id)
            form = FormLei(instance=leis)
        else:
            form = FormLei()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, condutor_id=None):

        if condutor_id:
            leis = Lei.objects.get(pk=condutor_id)
            form = FormLei(instance=leis, data=request.POST)
        else:

            form = FormLei(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaLeisView(View):
    template_name = 'leis/consulta.html'

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

        leis_page = Lei.objects.get_page(page, procurar)

        return render(request, self.template_name, {'leis': leis_page, 'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):

        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):

        return self.__page(request)
