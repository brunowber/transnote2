from rest_framework import serializers

from agente import AgenteSerializer
from bloco import BlocoSerializer
from cidade import CidadeSerializer
from especie import EspecieSerializer
from modelo import ModeloSerializer
from proprietario import ProprietarioSerializer
from regiao import RegiaoSerializer
from tipo_infracao import TipoInfracaoSerializer
from tipo_veiculo import TipoVeiculoSerializer
from uf import UFSerializer
from veiculo import VeiculoSerializer, VeiculoPageSerializer
from cor import CorSerializer
from categoria import CategoriaSerializer
from config_sinc import ConfigSincSerializer
from detransapp.models import Agente


class SnippetSerializer(serializers.Serializer):
    identificacao = serializers.CharField(max_length=6)
    nome = serializers.CharField(max_length=100)

    @staticmethod
    def restore_object(attrs, instance=None):
        """
             Cria ou faz a atualizacao de uma nova instancia de um modelo,
             dado um dicionario de campos nao seriados.

             Caso esse metodo nao exista, o retorno sera sempe um dicionario de itens.
        """
        if instance:
            # Update existing instance
            instance.identificacao = attrs.get(
                'identificacao', instance.identificacao)
            instance.nome = attrs.get('nome', instance.nome)
            return instance

        # Cria nova instancia
        return Agente(**attrs)
