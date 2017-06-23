from rest_framework import serializers
from detransapp.models import Veiculo


class VeiculoSerializer(serializers.Serializer):
    renavam = serializers.IntegerField()
    chassi = serializers.CharField(max_length=21)
    nr_motor = serializers.CharField(max_length=21)
    placa = serializers.CharField(max_length=7)
    modelo_id = serializers.IntegerField()
    tipo_veiculo_id = serializers.IntegerField()
    especie_id = serializers.IntegerField()
    cidade_id = serializers.IntegerField()
    cor_id = serializers.IntegerField()
    categoria_id = serializers.IntegerField()
    ano_fabricacao = serializers.IntegerField()
    ano_modelo = serializers.IntegerField()
    num_passageiro = serializers.CharField(max_length=3)

    @staticmethod
    def restore_object(attrs, instance=None):
        if instance:
            instance.renavem = attrs.get('renavam', instance.renavam)
            instance.placa = attrs.get('placa', instance.placa)
            instance.modelo_id = attrs.get('modelo_id', instance.modelo_id)
            instance.tipo_veiculo_id = attrs.get('tipo_veiculo_id', instance.tipo_id)
            instance.especie_id = attrs.get('especie_id', instance.especie_id)
            instance.cidade_id = attrs.get('cidade_id', instance.cidade_id)
            instance.cor_id = attrs.get('cor_id', instance.cor_id)
            instance.categoria_id = attrs.get('categoria_id', instance.categoria_id)
            instance.ano_fabricacao = attrs.get('ano_fabricacao', instance.ano_fabricacao)
            instance.ano_modelo = attrs.get('ano_modelo', instance.ano_modelo)
            instance.num_passageiro = attrs.get('num_passageiro', instance.num_passageiro)

            return instance

        return Veiculo(**attrs)


class VeiculoPageSerializer(serializers.Serializer):
    num_pages = serializers.IntegerField()
    number = serializers.IntegerField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.num_pages = attrs.get('num_pages', instance.num_pages)
            instance.number = attrs.get('number', instance.number)

            return instance

        return Veiculo(**attrs)
