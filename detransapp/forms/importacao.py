# coding: utf-8
"""Formulario de importação"""
from django import forms


class FormArquivo(forms.Form):
    """Classes de importação"""

    arquivo = forms.FileField()
