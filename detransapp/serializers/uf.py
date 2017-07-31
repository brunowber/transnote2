from rest_framework import serializers
from detransapp.models import UF


class UFSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sigla = serializers.CharField(max_length=2)
    nome = serializers.CharField(max_length=50)

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.id = attrs.get('id', instance.id)
            instance.sigla = attrs.get('sigla', instance.sigla)
            instance.nome = attrs.get('nome', instance.nome)
            return instance

        return UF(**attrs)
