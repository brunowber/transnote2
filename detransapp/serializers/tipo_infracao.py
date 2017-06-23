from rest_framework import serializers

from detransapp.models import TipoInfracao


class TipoInfracaoSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=20)
    descricao = serializers.CharField(max_length=40)
    is_condutor_obrigatorio = serializers.BooleanField()
    ativo = serializers.BooleanField()
    lei_id = serializers.IntegerField()

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.codigo = attrs.get('codigo', instance.codigo)
            instance.descricao = attrs.get('descricao', instance.descricao)
            instance.is_condutor_obrigatorio = attrs.get\
                ('is_condutor_obrigatorio', instance.is_condutor_obrigatorio)
            instance.ativo = attrs.get('ativo', instance.ativo)
            instance.lei_id = attrs.get('lei_id', instance.lei_id)
            return instance

        return TipoInfracao(**attrs)
