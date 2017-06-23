# coding: utf-8
"""Formulario de tipos de infração"""

from django import forms

from detransapp.models import TipoInfracao


class FormTipoInfracao(forms.ModelForm):
    """Classes de tipos de infrção"""

    class Meta:
        model = TipoInfracao
        fields = "__all__"
