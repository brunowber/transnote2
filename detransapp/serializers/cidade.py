from rest_framework import serializers
from detransapp.models import Cidade


class CidadeSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    nome = serializers.CharField(max_length=40)
    uf_id = serializers.IntegerField()

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.id = attrs.get('codigo', instance.codigo)
            instance.nome = attrs.get('nome', instance.nome)
            instance.uf_id = attrs.get('uf_id', instance.uf_id)
            return instance

        return Cidade(**attrs)
