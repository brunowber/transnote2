# coding: utf-8
"""Formulario de cores"""

from django import forms

from detransapp.models import Cor


class FormCor(forms.ModelForm):
    """Classes de cores"""

    class Meta:
        model = Cor
        fields = "__all__"
