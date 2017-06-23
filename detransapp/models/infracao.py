# coding: utf-8
"""Model para infrações"""

from django.db import models
from detransapp.models.tipo_infracao import TipoInfracao
from detransapp.models.infrator import Infrator
from detransapp.models.agente import Agente
from detransapp.models.veiculo import Veiculo
from detransapp.models.movimentacao import Movimentacao
from detransapp.models.tipo_cancelamento import TipoCancelamento
from detransapp.models.dispositivo import Dispositivo
from detransapp.manager import InfracaoManager


class Infracao(models.Model):
    """Classe para models de infrações"""

    id = models.IntegerField(primary_key=True)
    tipo_infracao = models.ForeignKey(TipoInfracao, null=True)
    infrator = models.ForeignKey(Infrator, null=True)
    agente = models.ForeignKey(Agente, null=True)
    veiculo = models.ForeignKey(Veiculo, null=True)
    obs = models.CharField(max_length=1000, null=True)
    movimento = models.ForeignKey(Movimentacao, null=True)

    is_estrangeiro = models.BooleanField()
    is_veiculo_editado = models.BooleanField()

    is_condutor_identi = models.BooleanField()
    is_cancelado = models.BooleanField(default=False)
    data_cancelamento = models.DateTimeField(null=True)
    motivo_cancelamento = models.CharField(max_length=255, null=True)

    tipo_cancelamento = models.ForeignKey(TipoCancelamento, null=True, blank=True)
    justificativa = models.CharField(max_length=255, null=True)
    dispositivo = models.ForeignKey(Dispositivo, null=True)

    local = models.CharField(max_length=255, null=True)
    local_numero = models.CharField(max_length=100, null=True)

    data_infracao = models.DateTimeField(null=True)
    data_sincronizacao = models.DateTimeField(auto_now=True)
    data_ocorrencia = models.DateTimeField(null=True)
    det = models.CharField(max_length=255, default='0')
    status_cnh = models.CharField(max_length=1, null=True)
    objects = InfracaoManager()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        app_label = "detransapp"
