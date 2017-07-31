# coding: utf-8
"""Formulario de configuração"""
from django import forms

from detransapp.models import ConfigSinc


class FormConfigSinc(forms.ModelForm):
    """Classes de configuração"""

    class Meta:
        model = ConfigSinc
        fields = "__all__"
