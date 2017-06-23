# coding: utf-8
"""Faz as operações para a carga inicial"""

import urllib2
import json

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from detransapp.models import Cidade, Modelo
from detransapp.serializers import CidadeSerializer
from detransapp.rest import JSONResponse


def carga_cadasdro():
    """Faz o cadastro da carga inicial"""
    # fipeapi.appspot.com API para consultar dados da FIPE
    
    response = urllib2.urlopen('http://fipeapi.appspot.com/api/1/carros/marcas.json')

    json_marcas = json.loads(response.read())

    for marca_json in json_marcas:

        if (Modelo.objects.filter(sigla=marca_json['name']).first()) is None:
            marca = Modelo(sigla=marca_json['name'], nome=marca_json['fipe_name'])
            marca.save()

    for marca_json in json_marcas:
        response = urllib2.urlopen(
            'http://fipeapi.appspot.com/api/1/carros/veiculos/%s.json' % (marca_json['id']))
        json_modelos = json.loads(response.read())

        marca = Modelo.objects.filter(sigla=marca_json['name']).first()

        for modelo_json in json_modelos:
            if (Modelo.objects.filter(nome=modelo_json['name'], marca_id=marca.id).first()) is None:
                modelo = Modelo(id=modelo_json['id'], nome=modelo_json['name'], marca_id=marca.id)
                modelo.save()

    return redirect('/')


class GetCidadesRestView(APIView):
    """Pega as cidades do servidor para a carga inicial"""

    permission_classes = (IsAuthenticated, AllowAny)

    def post(self, request):
        """Devolve para a carga inicial as cidades"""

        cidades = Cidade.objects.filter(uf_id=int(request.POST['uf_id']))
        json_cidades = []
        for estado in cidades:
            serializer = CidadeSerializer(estado)
            json_cidades.append(serializer.data)

        return JSONResponse(json_cidades)
