from rest_framework import serializers
from detransapp.models import Modelo


class ModeloSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    descricao = serializers.CharField(max_length=40)

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.codido = attrs.get('codigo', instance.codigo)
            instance.descrciao = attrs.get('descricao', instance.descricao)
            return instance

        return Modelo(**attrs)
