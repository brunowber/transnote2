from rest_framework import serializers
from detransapp.models import Proprietario


class ProprietarioSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cnh = serializers.CharField(max_length=11)
    nome = serializers.CharField(max_length=60)
    documento = serializers.CharField(max_length=14)

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.id = attrs.get('id', instance.id)
            instance.cnh = attrs.get('cnh', instance.cnh)
            instance.nome = attrs.get('nome', instance.nome)
            instance.documento = attrs.get('documento', instance.documento)

            return instance

        return Proprietario(**attrs)
