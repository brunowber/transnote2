# coding: utf-8
"""Formulario de modelos"""

from django import forms

from detransapp.models import Modelo


class FormModelo(forms.ModelForm):
    """Classe de modelos"""

    class Meta:
        model = Modelo
        fields = "__all__"
