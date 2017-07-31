from rest_framework import serializers
from detransapp.models import Categoria


class CategoriaSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    descricao = serializers.CharField(max_length=40)

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.codigo = attrs.get('codigo', instance.codigo)
            instance.descricao = attrs.get('descricao', instance.descricao)
            return instance

        return Categoria(**attrs)
