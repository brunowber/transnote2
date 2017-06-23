# coding: utf-8
"""Formulario de leis"""

from django import forms

from detransapp.models.lei import Lei


class FormLei(forms.ModelForm):
    # coding: utf-8
    """Classes de leis"""

    class Meta:
        model = Lei
        fields = "__all__"
