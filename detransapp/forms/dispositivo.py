# coding: utf-8
"""Formulario de dispositivos"""

from django import forms

from detransapp.models import Dispositivo


class FormDispositivo(forms.ModelForm):
    """Classes de dispositivos"""

    class Meta:
        model = Dispositivo
        fields = "__all__"
