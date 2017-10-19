#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Formulario de agentes"""

from django import forms
from detransapp.models import Agente


class FormAgente(forms.ModelForm):
    """Classes para agentes"""

    password = forms.CharField(widget=forms.PasswordInput)
    permissao_geral = forms.BooleanField(initial=False, required=False)

    def save(self, commit=True):
        agente = super(FormAgente, self).save(commit=False)
        agente.set_password(self.cleaned_data['password'])
        if commit:
            agente.save()
        return agente

    def clean(self):
        cont = 0
        try:
            senha = self.cleaned_data['password']
            print senha
        except Exception as e:
            print e
            msg = 'Este campo é obrigatório.'
            self._errors['password'] = self.error_class([msg])
            raise forms.ValidationError("")
        if senha in self.cleaned_data['first_name']:
            msg = 'Seu nome não pode conter na senha.'
            self._errors['password'] = self.error_class([msg])
        if len(senha) < 8:
            msg = 'Senha possui tem que possuir ao menos 8 digítos.'
            self._errors['password'] = self.error_class([msg])
        for digito in senha:
            if digito.isdecimal():
                cont += 1
                break
        for digito in senha:
            if digito.isupper():
                cont += 1
                break
        for digito in senha:
            if digito.islower():
                cont += 1
                break
        for digito in senha:
            if digito in "!@#$%*.":
                cont += 1
                break
        if cont < 2:
            msg = 'Senha muito simples, tente outra.'
            self._errors['password'] = self.error_class([msg])

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if Agente.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Esse CPF já existe.")
        if len(cpf) != 11:
            raise forms.ValidationError("CPF possui exatamente 11 digítos.")
        d1 = 0
        d2 = 0
        i = 0
        while i < 10:
            d1, d2, i = (d1 + (int(cpf[i]) * (11 - i - 1))) % 11 if i < 9 else d1, (
                d2 + (int(cpf[i]) * (11 - i))) % 11, i + 1
        if not ((int(cpf[9]) == (11 - d1 if d1 > 1 else 0)) and (int(cpf[10]) == (11 - d2 if d2 > 1 else 0))):
            raise forms.ValidationError("CPF inválido")
        return cpf

    class Meta:
        model = Agente
        exclude = ('movimentos', 'regioes', 'email', 'date_joined',
                   'is_staff', 'user_permissions', 'last_login',)
