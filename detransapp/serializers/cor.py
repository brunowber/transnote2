from rest_framework import serializers
from detransapp.models import Cor


class CorSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    descricao = serializers.CharField(max_length=40)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.codigo = attrs.get('codigo', instance.codigo)
            instance.descricao = attrs.get('descricao', instance.descricao)
            return instance

        return Cor(**attrs)
