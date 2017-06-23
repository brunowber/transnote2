# coding: utf-8
"""Teoricamente é para cadastrar a infração"""
import random

from django.shortcuts import redirect
from django.utils import timezone

from detransapp.models import Agente, Veiculo, Movimentacao, Infracao, TipoInfracao

def cad():
    """Cadastra infrações"""
    tipo = TipoInfracao.objects.all()[0]
    # condutor = Condutor.objects.all()[0]
    agente = Agente.objects.all()[0]
    veiculo = Veiculo.objects.all()[0]
    moviment = Movimentacao(tempo=timezone.now(), latitude=1.56,
                            longitude=1.32)
    moviment.save()
    number = random.randint(0, 100000000000000000000000000000000)
    inf = Infracao(tipo=tipo, agente=agente, veiculo=veiculo, id_sincronia=number,
                   tempo=timezone.now(), movimento=moviment, data_infracao=timezone.now())

    inf.save()
    return redirect('/')
