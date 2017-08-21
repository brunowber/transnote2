# coding: utf-8
"""View para CRUD de cidades"""

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from detransapp.models import Cidade, UF
from detransapp.serializers import CidadeSerializer
from detransapp.rest import JSONResponse
from detransapp.decorators import validar_imei
from detransapp.forms.importacao import FormArquivo
from detransapp.decorators import permissao_geral_required


@csrf_exempt
def get_cidades(request):
    """Pega as cidades e envia para a página"""
    cidades = Cidade.objects.filter(uf_id=request.POST['uf']).order_by('nome')
    cidades_json = serializers.serialize('json', cidades)
    return HttpResponse(cidades_json)


class GetCidadesRestView(APIView):
    """Pega as cidades para mostrar no Android"""

    permission_classes = (IsAuthenticated, AllowAny)

    @method_decorator(validar_imei())
    def post(self, request):
        """Envia a páginação das cidades para o Android"""

        if 'data' in request.POST:
            cidades = Cidade.objects.get_cidades_sicronismo(int(request.POST['uf_id'])
                                                            , request.POST['data'])
        else:
            cidades = Cidade.objects.get_cidades_sicronismo(int(request.POST['uf_id']))
        json_cidades = []
        for estado in cidades:
            serializer = CidadeSerializer(estado)
            json_cidades.append(serializer.data)

        return JSONResponse(json_cidades)


class ImportaCidade(View):
    """Importa as cidades"""

    template_name = 'cidade/importa.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        """Envia um formulário para o template"""

        form = FormArquivo()

        return render(request, self.template_name, {'form': form})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        """Envia o arquivo importado para o servidor"""
        arq = request.FILES['arquivo']
        i = 0
        estado = UF.objects.filter(sigla='SC').first()

        if estado is None:
            estado = UF(sigla='SC', nome='Santa Catarina')
            estado.save()

        for linha in arq:
            try:
                linha = linha.encode('UTF-8')
                cod = int(linha[:4])
                cidade = linha[4:44].strip()
                nova_cidade = Cidade(uf_id=estado.id, codigo=cod, nome=cidade)
                nova_cidade.save()
                i += 1
            except Exception:
                continue

        return render(request, self.template_name, {'qtd': i, 'envio': True})
