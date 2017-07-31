from rest_framework import serializers
from detransapp.models import Regiao


class RegiaoSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=50)
    id = serializers.IntegerField()

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.nome = attrs.get('nome', instance.nome)
            instance.id = attrs.get('id', instance.id)
            return instance

        return Regiao(**attrs)
