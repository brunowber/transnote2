# coding: utf-8
"""Formulario de proprietarios"""

from django import forms

from detransapp.models import Proprietario


class FormProprietario(forms.ModelForm):
    """Classe de proprietarios"""

    class Meta:
        model = Proprietario
        fields = "__all__"
