from rest_framework import serializers
from detransapp.models import Agente


class AgenteSerializer(serializers.Serializer):
    identificacao = serializers.CharField(max_length=6)
    username = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)
    id = serializers.IntegerField()

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.identificacao = attrs.get('identificacao', instance.identificacao)
            instance.password_app = attrs.get('password', instance.password)
            instance.username = attrs.get('username', instance.username)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.id = attrs.get('id', instance.id)
            return instance

        return Agente(**attrs)
