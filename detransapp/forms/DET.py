# coding: utf-8
"""Formulario de DETs"""

from django import forms

from detransapp.models.DET import Configuracao_DET


class FormDet(forms.ModelForm):
    """Classes de DETs"""

    class Meta:
        model = Configuracao_DET
        fields = "__all__"
