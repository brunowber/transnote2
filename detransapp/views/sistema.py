# coding: utf-8
"""Arruma as opções do sistema"""
from django.views.generic.base import View
from django.shortcuts import render, redirect
from detransapp.forms.logo_form import LogoForm
from detransapp.models.sistema import Sistema
from django.utils.decorators import method_decorator
from detransapp.decorators import permissao_geral_required


class UploadDetransLogoView(View):
    """View que faz um upload da logo para o servidor"""
    template = 'upload/logo.html'

    @method_decorator(permissao_geral_required())
    def get(self, request, sistema_id=None):
        """Envia o template para fazer a mudança do logo"""

        if len(Sistema.objects.filter()) > 0:
            sistema = Sistema.objects.last()
            sistema_id = sistema.id

        if sistema_id:
            print 'aqui'
            sistema = Sistema.objects.get(pk=sistema_id)
            form = LogoForm(instance=sistema)

        else:
            print 'else'
            form = LogoForm()

        return render(request, self.template, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        """Envia a imagem para ser usada como logo"""

        sistema = Sistema.objects.filter()
        arquivos = ['jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG']
        if len(sistema) > 0:
            if not request.FILES:
                sistema_id = Sistema.objects.latest('id').id
                sistema = Sistema.objects.get(pk=sistema_id)
                form = LogoForm(request.POST or None, request.FILES or None, instance=sistema)
                form.logo = sistema.logo
            else:
                sistema_id = Sistema.objects.latest('id').id
                sistema = Sistema.objects.get(pk=sistema_id)
                form = LogoForm(request.POST or None, request.FILES or None, instance=sistema)
        else:
            form = LogoForm(request.POST or None, request.FILES or None)
        if sistema.logo or 'logo' in request.FILES and str(request.FILES['logo']).split('.')[-1] in arquivos:
            print 'if'
            if form not in globals():
                form = LogoForm(request.POST or None, request.FILES or None, instance=sistema)
            if form.is_valid():
                form.save(request)
                return redirect('/')
            else:
                return render(request, self.template, {'form': form})
        else:
            if form not in globals():
                form = LogoForm(instance=Sistema.objects.latest('id'))
            return render(request, self.template, {'form': form, 'erro': 'erro'})
