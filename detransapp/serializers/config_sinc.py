from rest_framework import serializers
from detransapp.models import ConfigSinc


class ConfigSincSerializer(serializers.Serializer):
    horas_descarte = serializers.IntegerField()
    tempo_captura_mov = serializers.IntegerField()
    distancia_captura_mov = serializers.DecimalField(
        max_digits=10, decimal_places=2)

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.horas_descarte = attrs.get('horas_descarte', instance.horas_descarte)
            instance.tempo_captura_mov = attrs.get('tempo_captura_mov', instance.tempo_captura_mov)
            instance.distancia_captura_mov = attrs.get('distancia_captura_mov',
                                                       instance.distancia_captura_mov)
            return instance

        return ConfigSinc(**attrs)
