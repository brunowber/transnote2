# coding: utf-8
"""Formulario de tipos de cancelamento"""

from django import forms

from detransapp.models import TipoCancelamento


class FormTipoCancelamento(forms.ModelForm):
    """Classe de tipos de cancelamento"""

    class Meta:
        model = TipoCancelamento
        fields = "__all__"
