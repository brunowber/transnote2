# coding: utf-8
"""CRUD do tipo de cancelamento"""

from django.shortcuts import render, redirect
from django.views.generic.base import View
from detransapp.forms.tipo_cancelamento import FormTipoCancelamento
from detransapp.models import TipoCancelamento
from django.utils.decorators import method_decorator
from detransapp.decorators import permissao_geral_required, autenticado

class CadastroCancelamentoView(View):
    """View para fazer CRUD dos tipos de cancelamento"""

    template = 'tipo_cancelamento/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, cancelamento_id=None):
        """Envia o formulário para o template"""

        if cancelamento_id:
            cancelamento = TipoCancelamento.objects.get(pk=cancelamento_id)
            form = FormTipoCancelamento(instance=cancelamento)
        else:
            form = FormTipoCancelamento()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, cancelamento_id=None):
        """Envia os valores do tipo de cancelamento para o
         banco de dados"""

        if cancelamento_id:
            cancelamento = TipoCancelamento.objects.get(pk=cancelamento_id)
            form = FormTipoCancelamento(instance=cancelamento, data=request.POST)
        else:

            form = FormTipoCancelamento(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaCancelamentoView(View):
    template_name = 'tipo_cancelamento/consulta.html'

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

        cancelamentos_page = TipoCancelamento.objects.get_page(page, procurar)

        return render(request, self.template_name, {'cancelamentos': cancelamentos_page,
                                                    'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):

        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):

        return self.__page(request)
