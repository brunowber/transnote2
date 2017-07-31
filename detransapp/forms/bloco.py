"""Formulario de blocos"""

from django import forms
from detransapp.models import BlocoPadrao


class FormBloco(forms.ModelForm):
    """Classes de blocos"""

    class Meta:
        model = BlocoPadrao
        fields = ('inicio_intervalo', 'fim_intervalo', 'ativo',
                  'numero_paginas', 'minimo_pag_restantes',)
