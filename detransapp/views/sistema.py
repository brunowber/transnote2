# coding: utf-8
"""Arruma as opções do sistema"""
from django.views.generic.base import View
from django.shortcuts import render, redirect
from detransapp.forms.logo_form import LogoForm
from detransapp.models.sistema import Sistema


class UploadDetransLogoView(View):
    """View que faz um upload do logo para o servidor"""
    template = 'upload/logo.html'

    def get(self, request, sistema_id=None):
        """Envia o template para fazer a mudança do logo"""

        sistema = Sistema.objects.filter()
        if len(sistema) > 0:
            sistema_id = sistema[0].id

        if sistema_id:
            sistema = Sistema.objects.get(pk=sistema_id)
            form = LogoForm(instance=sistema)

        else:
            form = LogoForm()

        return render(request, self.template, {'form': form})

    def post(self, request):
        """Envia a imagem para ser usada como logo"""

        sistema = Sistema.objects.filter()
        arquivos = ['jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG']
        if len(sistema) > 0:
            sistema_id = sistema[0].id
            sistema = Sistema.objects.get(pk=sistema_id)
            form = LogoForm(request.POST or None, request.FILES or None, instance=sistema)
        if 'logo' in request.FILES and str(request.FILES['logo']).split('.')[-1] in arquivos:
            if form not in globals():
                form = LogoForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save(request)
                return redirect('/')
            else:
                return render(request, self.template, {'form': form})
        else:
            if form not in globals():
                form = LogoForm(instance=sistema)
            return render(request, self.template, {'form': form, 'erro': 'erro'})
