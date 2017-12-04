# coding: utf-8
"""Arquivo para cadastrar dipositivo"""
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from detransapp.decorators import permissao_geral_required, autenticado
from detransapp.forms.dispositivo import FormDispositivo
from detransapp.models import Dispositivo, Acesso


class CadastroDispositivoView(View):
    """Cadastra os dispositivos"""
    template = 'dispositivo/salvar.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, dispositivo_id=None):
        """Cria um formulário para cadastrar o dispositivo"""

        if dispositivo_id:
            dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
            form = FormDispositivo(instance=dispositivo)
        else:
            form = FormDispositivo()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request, dispositivo_id=None):
        """Envia para o servidor os dispositivos cadastrados"""

        if dispositivo_id:
            dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
            form = FormDispositivo(instance=dispositivo, data=request.POST)
        else:

            form = FormDispositivo(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')

        return render(request, self.template, {'form': form})


class ConsultaDispositivoView(View):
    """Consulta os dispositivos cadastrados"""

    template_name = 'dispositivo/consulta.html'

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

        dispositivoes_page = Dispositivo.objects.get_page(page, procurar)

        return render(request, self.template_name, {'dispositivos': dispositivoes_page,
                                                    'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):
        """Pega a primeira página"""

        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):
        """Pesquisa o dispositivo"""

        return self.__page(request)


class ConsultaDispositivoAcessoView(View):
    """Consulta os dispositivos cadastrados"""

    template_name = 'dispositivo/acesso.html'

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

        dispositivoes_page = Acesso.objects.get_page(page, procurar)

        return render(request, self.template_name, {'dispositivos': dispositivoes_page,
                                                    'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):
        """Pega a primeira página"""
        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):
        """Pesquisa o dispositivo"""

        return self.__page(request)


class CadastroDispositivoAcessoView(View):
    """Cadastra os dispositivos"""
    template_name = 'dispositivo/acesso.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, dispositivo_id=None):
        """Cadastra o acesso"""

        if dispositivo_id:
            acesso = Acesso.objects.get(pk=dispositivo_id)
            dispositivo = Dispositivo.objects.get_or_create(imei=acesso.imei)[0]
            dispositivo.ativo = True
            dispositivo.save()
            Acesso.objects.get(pk=dispositivo_id).delete()

        return redirect('/dispositivo/acesso/')


class RemoveDispositivoAcessoView(View):
    """Remove os dispositivos"""
    template_name = 'dispositivo/acesso.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, dispositivo_id=None):
        """Remove o acesso"""

        Acesso.objects.get(pk=dispositivo_id).delete()

        return redirect('/dispositivo/acesso/')


class ConsultaDispositivoAcessoView(View):
    """Consulta os dispositivos nao cadastrados"""

    template_name = 'dispositivo/acesso.html'

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
            
        return render(request, self.template_name, {'dispositivos': dispositivoes_page,
                                                    'procurar': procurar})

    @method_decorator(autenticado())
    def get(self, request):
        """Pega a primeira página"""

        return self.__page(request)

    @method_decorator(autenticado())
    def post(self, request):
        """Pesquisa o dispositivo"""

        return self.__page(request)