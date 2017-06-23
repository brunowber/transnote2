# coding: utf-8
"""Formulario de infrator"""

from django import forms

from detransapp.models import Infrator


class FormInfrator(forms.ModelForm):
    """Classes de infrator"""

    class Meta:
        model = Infrator
        fields = "__all__"
