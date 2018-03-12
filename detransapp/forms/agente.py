#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Formulario de agentes"""

import string
from django import forms
from detransapp.models import Agente


class FormAgente(forms.ModelForm):
    """Classes para agentes"""

    password = forms.CharField(widget=forms.PasswordInput, max_length=30)
    permissao_geral = forms.BooleanField(initial=False, required=False)

    def save(self, commit=True):
        agente = super(FormAgente, self).save(commit=False)
        agente.set_password(self.cleaned_data['password'])
        if commit:
            agente.save()
        return agente

    def clean(self):
        try:
            senha = self.cleaned_data['password']
            if len(senha) < 8:
                msg = 'Senha possui tem que possuir ao menos 8 digítos.'
                self._errors['password'] = self.error_class([msg])
            cont, decimal, upper, lower, symbol = 0, True, True, True, True
            for digito in senha:
                if digito.isdecimal() and decimal:
                    cont += 1
                    decimal = False
                if digito.isupper() and upper:
                    cont += 1
                    upper = False
                if digito.islower() and lower:
                    cont += 1
                    lower = False
                if digito in string.punctuation and symbol:
                    cont += 1
                    symbol = False
            if cont < 3:
                msg = 'Senha muito simples, tente outra.'
                self._errors['password'] = self.error_class([msg])
        except Exception:
            msg = 'Este campo é obrigatório.'
            self._errors['password'] = self.error_class([msg])
        try:
            nome = self.cleaned_data['first_name']
            if nome == "":
                msg = "Este campo é obrigatório."
                self._errors['first_name'] = self.error_class([msg])

            for digito in nome:
                if digito.isdecimal():
                    msg = "Nome deve conter apenas letras."
                    self._errors['first_name'] = self.error_class([msg])
        except Exception:
            msg = 'Este campo é obrigatório.'
            self._errors['first_name'] = self.error_class([msg])
        try:
            if nome.lower() in senha.lower() and nome != "":
                msg = 'Seu nome não pode conter na senha.'
                self._errors['password'] = self.error_class([msg])
        except Exception:
            print ("sem nome ou senha")

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        for digito in cpf:
            if not digito.isdecimal():
                raise forms.ValidationError("CPF deve conter somente números.")
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

    def clean_identificacao(self):
        identificacao = self.cleaned_data['identificacao']
        if Agente.objects.filter(identificacao=identificacao):
            raise forms.ValidationError("Esse número de identificação já está em uso.")
        for digito in identificacao:
            if not digito.isdecimal():
                raise forms.ValidationError("Identificação deve conter somente números.")
        if Agente.objects.filter(identificacao=identificacao).exists():
            raise forms.ValidationError("Essa identificação já está em uso.")
        agente = Agente.objects.filter()
        for i in agente:
            print i.identificacao
        return identificacao

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 8:
            raise forms.ValidationError("Usuário dever conter ao menos 8 dígitos.")
        if not Agente.objects.filter(username=username):
            return username.lower()
        if Agente.objects.filter(username=username).exists():
            print "teste"
            raise forms.ValidationError("Esse usuário já está em uso.")

    class Meta:
        model = Agente
        exclude = ('movimentos', 'regioes', 'email', 'date_joined',
                   'is_staff', 'user_permissions', 'last_login',)


class FormAgenteEdit(forms.ModelForm):
    """Classes para agentes"""

    password = forms.CharField(widget=forms.PasswordInput, max_length=30)
    permissao_geral = forms.BooleanField(initial=False, required=False)

    def save(self, commit=True):
        agente = super(FormAgenteEdit, self).save(commit=False)
        agente.set_password(self.cleaned_data['password'])
        if commit:
            agente.save()
        return agente

    def clean(self):
        identificacao = self.cleaned_data['identificacao']
        agente = Agente.objects.get(identificacao=identificacao)
        try:
            cpf = self.cleaned_data['cpf']
            if agente.cpf != cpf:
                if Agente.objects.filter(cpf=cpf).exists():
                    msg = "Esse CPF já está em uso."
                    self._errors['cpf'] = self.error_class([msg])
                else:
                    for digito in cpf:
                        if not digito.isdecimal():
                            msg = "CPF deve conter somente números."
                            self._errors['cpf'] = self.error_class([msg])
                    if len(cpf) != 11:
                        msg = "CPF possui exatamente 11 digítos."
                        self._errors['cpf'] = self.error_class([msg])
                d1 = 0
                d2 = 0
                i = 0
                print "aqui"
                while i < 10:
                    d1, d2, i = (d1 + (int(cpf[i]) * (11 - i - 1))) % 11 if i < 9 else d1, (
                        d2 + (int(cpf[i]) * (11 - i))) % 11, i + 1
                if not ((int(cpf[9]) == (11 - d1 if d1 > 1 else 0)) and (int(cpf[10]) == (11 - d2 if d2 > 1 else 0))):
                    msg = "CPF inválido."
                    self._errors['cpf'] = self.error_class([msg])
        except Exception:
            print "Erro CPF"

        try:
            username = self.cleaned_data['username']
            if agente.username != username:
                print agente.username, username
                if Agente.objects.filter(username=username).exists():
                    print Agente.objects.filter(username=username)
                    msg = "Esse usuário já está em uso."
                    self._errors['username'] = self.error_class([msg])
                if len(username) < 8:
                    msg = "Usuário dever conter ao menos 8 dígitos."
                    self._errors['username'] = self.error_class([msg])
        except Exception:
            print "Erro username"

        try:
            senha = self.cleaned_data['password']
            if len(senha) < 8:
                msg = 'Senha possui tem que possuir ao menos 8 digítos.'
                self._errors['password'] = self.error_class([msg])
            cont, decimal, upper, lower, symbol = 0, True, True, True, True
            for digito in senha:
                if digito.isdecimal() and decimal:
                    cont += 1
                    decimal = False
                if digito.isupper() and upper:
                    cont += 1
                    upper = False
                if digito.islower() and lower:
                    cont += 1
                    lower = False
                if digito in string.punctuation and symbol:
                    cont += 1
                    symbol = False
            if cont < 3:
                msg = 'Senha muito simples, tente outra.'
                self._errors['password'] = self.error_class([msg])
        except Exception:
            msg = 'Este campo é obrigatório.'
            self._errors['password'] = self.error_class([msg])
        try:
            nome = self.cleaned_data['first_name']
            if nome == "":
                msg = "Este campo é obrigatório."
                self._errors['first_name'] = self.error_class([msg])

            for digito in nome:
                if digito.isdecimal():
                    msg = "Nome deve conter apenas letras."
                    self._errors['first_name'] = self.error_class([msg])
        except Exception:
            msg = 'Este campo é obrigatório.'
            self._errors['first_name'] = self.error_class([msg])
        try:
            if nome.lower() in senha.lower() and nome != "":
                msg = 'Seu nome não pode conter na senha.'
                self._errors['password'] = self.error_class([msg])
        except Exception:
            print ("sem nome ou senha")

    class Meta:
        model = Agente
        exclude = ('movimentos', 'regioes', 'email', 'date_joined',
                   'is_staff', 'user_permissions', 'last_login',)