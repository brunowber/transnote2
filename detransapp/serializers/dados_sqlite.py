from rest_framework import serializers
from detransapp.models import Detrans_sqlite


class DadosSqliteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    data_versao = serializers.DateTimeField()

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.data_inicio = attrs.get('data_versao', instance.data_versao)
            instance.id = attrs.get('id', instance.id)
            return instance

        return Detrans_sqlite(**attrs)
