"""Tela do Admin"""

from django.contrib import admin

from detransapp.models import Cidade, Veiculo,\
    Infracao, Infrator, Agente, Movimentacao, TipoVeiculo,\
    TipoInfracao, Dispositivo, Sistema, Lei, Especie, Categoria, UF,\
    Configuracao_DET, Regiao, Modelo, Cor, DET, Agente_login, Bloco,\
    BlocoPadrao, ConfigSinc, VeiculoEditado


admin.site.register(Cidade)
admin.site.register(Veiculo)
admin.site.register(Infracao)
admin.site.register(Infrator)
admin.site.register(Agente)
admin.site.register(Movimentacao)
admin.site.register(TipoVeiculo)
admin.site.register(TipoInfracao)
admin.site.register(Dispositivo)
admin.site.register(Sistema)
admin.site.register(Lei)
admin.site.register(Especie)
admin.site.register(Categoria)
admin.site.register(UF)
admin.site.register(Configuracao_DET)
admin.site.register(Regiao)
admin.site.register(Modelo)
admin.site.register(Cor)
admin.site.register(DET.DET)
admin.site.register(Agente_login)
admin.site.register(Bloco)
admin.site.register(ConfigSinc)
admin.site.register(BlocoPadrao)
admin.site.register(VeiculoEditado)
