# coding: utf-8
"""Formulario de especies"""

from django import forms

from detransapp.models import Especie


class FormEspecie(forms.ModelForm):
    """Classes de especies"""

    class Meta:
        model = Especie
        fields = "__all__"
