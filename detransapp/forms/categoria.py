"""Formulario de categorias"""

from django import forms

from detransapp.models import Categoria


class FormCategoria(forms.ModelForm):
    """Classes de categorias"""

    class Meta:
        model = Categoria
        fields = "__all__"
