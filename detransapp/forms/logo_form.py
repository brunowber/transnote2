# coding: utf-8
"""Formulario das logos"""
from django import forms
from detransapp.models.sistema import Sistema


class LogoForm(forms.ModelForm):
    """Classe das logos"""
    class Meta:
        model = Sistema
        fields = ['sigla', 'nome_completo', 'logo',]