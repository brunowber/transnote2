# coding: utf-8
"""Formulario de upload do apk"""

from django import forms
from detransapp.models.config_sinc import ConfigSinc


class UploadApkForm(forms.ModelForm):
    """Classe do upload de apk"""

    class Meta:
        model = ConfigSinc
        fields = ['caminho_apk', ]
