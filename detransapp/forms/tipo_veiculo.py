# coding: utf-8
"""Formulario de tipos de veiculos"""

from django import forms

from detransapp.models import TipoVeiculo


class FormTipoVeiculo(forms.ModelForm):
    """classe de tipos de veiculos"""

    class Meta:
        model = TipoVeiculo
        fields = "__all__"
