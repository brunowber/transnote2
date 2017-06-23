from rest_framework import serializers
from detransapp.models import Bloco


class BlocoSerializer(serializers.Serializer):
    inicio_intervalo = serializers.IntegerField()
    fim_intervalo = serializers.IntegerField()
    ativo = serializers.BooleanField(default=True)
    minimo_pag_restantes = serializers.IntegerField()

    class Meta:
        model = Bloco
        fields = ('inicio_intervalo', 'fim_intervalo', 'data', 'data_alterado', 'ativo',
                  'usuario', 'agente_campo', 'minimo_pag_restantes',)
