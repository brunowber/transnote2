from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.db import connection

from detransapp.views.modelo import *
from detransapp.views.tipo_veiculo import *
from detransapp.views.tipo_infracao import *
from detransapp.views.especie import *
from detransapp.views.agente import *
from detransapp.views.veiculo import *
from detransapp.views.condutor import *
from detransapp.views.proprietario import *
from detransapp.views.dispositivo import *
from detransapp.views.infracao import *
from detransapp.views.regiao import *
from detransapp.views.uf import *
from detransapp.views.cidade import *
from detransapp.views.sincronismo import *
from detransapp.views.leis import *
from detransapp.views.bloco import *
from detransapp.views.cor import *
from detransapp.views.categoria import *
from detransapp.views.tipo_cancelamento import *
from detransapp.views.download_detrans import *
from detransapp.views.config_sinc import *
from detransapp.views.detrans_arquivo_sqlite import *
from detransapp.views.DET import *
from detransapp.views.sistema import *
import detransapp.views.cadastra_inf
from detransapp.models import *


def naoSinc():
    startdate = timezone.now() - timedelta(days=1)
    enddate = timezone.now()
    agts = Agente.objects.all()
    td = Infracao.objects.filter(data_infracao__range=[startdate, enddate])
    sinc = []
    ns = []
    for i in td:
        sinc.append(i.agente)
    for a in agts:
        if a not in sinc:
            ultima = Infracao.objects.filter(agente_id=a.id)
            if ultima:
                ultima = ultima[0]
                print(ultima.data_sincronizacao)
                ns.append({'agente': a, 'tempo': ultima.data_sincronizacao})
            else:
                ns.append({'agente': a})

    if len(ns) >= 5:
        ns = ns[:5]
    return ns


def graficoInfracoes():
    horas = {"data": """strftime('%H', data_infracao)"""}
    d = Infracao.objects.extra(select=horas).values('data').annotate(Count('data_infracao')).order_by('-data')
    return d


def ultimasSinc():
    return Infracao.objects.order_by('-data_infracao')[:5]


def grafico1():
    return


def ultimaHora():
    startdate = timezone.now() - timedelta(hours=1)
    enddate = timezone.now()
    return Infracao.objects.filter(data_infracao__range=[startdate, enddate]).annotate(Count('agente')).order_by(
        'data_infracao')[:5]


def diario():
    return None
    weekday = {"data": """strftime('%d/%m/%Y', data_infracao)"""}
    d = Infracao.objects.extra(select=weekday).values('data').annotate(Count('data_infracao')).order_by('-data')
    if len(d) >= 5:
        return d[0:5]
    else:
        return d


@login_required
def index(request):

    cursor = connection.cursor()

    #sql = 'CREATE SEQUENCE public.detransapp_detrans_sqlite_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;'
    #cursor.execute(sql)
    # sql = "CREATE TABLE detransapp_detrans_sqlite (id INTEGER NOT NULL DEFAULT nextval('detransapp_detrans_sqlite_id_seq'::regclass), data_versao CHAR NOT NULL, dt_acesso timestamp NOT NULL, usuario CHAR NOT NULL , CONSTRAINT detransapp_acesso_pkey PRIMARY KEY (id))"
    #sql = "CREATE TABLE detransapp_detrans_sqlite (id INTEGER NOT NULL DEFAULT nextval('detransapp_detrans_sqlite_id_seq'::regclass), data_versao timestamp NOT NULL, data_fim timestamp NOT NULL, finished BOOLEAN NOT NULL DEFAULT FALSE , CONSTRAINT detransapp_detrans_sqlite_pkey PRIMARY KEY (id))"
    #cursor.execute(sql)

    return render_to_response("index.html", RequestContext(request, {'ultimasSinc': ultimasSinc(), 'naoSinc': naoSinc(),
                                                                     'diario': diario(), 'ultimaHora': ultimaHora(),
                                                                     'graficoInfracoes': graficoInfracoes()}))


@login_required
def relatorios(request):
    return render_to_response('relatorios.html', RequestContext(request))

@login_required
def about(request):
    return render_to_response("sobre.html", RequestContext(request))