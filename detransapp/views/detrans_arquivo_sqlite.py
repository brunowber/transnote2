# coding: utf-8
"""Status de geração do SQlite"""
import threading
import sqlite3
from datetime import datetime
import os
from pysqlcipher import dbapi2 as sqliteCipher
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.conf import settings
from detrans_sqlite.importa import *
from detrans_sqlite import cria_db
from django.utils.decorators import method_decorator
from detransapp.decorators import permissao_geral_required
from detransapp.models.detrans_sqlite import Detrans_sqlite


class ThreadDetransSqlite(threading.Thread):
    # tempo com os ifs 10:35 as 11:12 = 37
    # tempo sem os ifs 11:55 as 12:33 = 37
    def __init__(self, threadName):

        threading.Thread.__init__(self)
        self.stopthread = threading.Event()
        self.threadName = threadName
        self.is_finalisado = False
        self.is_cancelado = False
        self.is_erro_processo = False
        self.progress = 0
        self.detrans_sqlite_nome = settings.MEDIA_ROOT + '/detrans.sqlite'
        self.detrans_sqlite_nome_execucao = settings.MEDIA_ROOT + '/detrans_execucao.sqlite'
        self.detrans_sqlite = Detrans_sqlite.objects.create()
        self.detrans_sqlite.data_versao = datetime.now()
        self.detrans_sqlite.usuario = "usuario"

    def run(self):

        try:
            self.progress = 1
            if os.path.exists(self.detrans_sqlite_nome_execucao):
                os.remove(self.detrans_sqlite_nome_execucao)

            self.progress = 1
            if os.path.exists(self.detrans_sqlite_nome_execucao + '.gz'):
                os.remove(self.detrans_sqlite_nome_execucao + '.gz')

            self.progress = 2
            conn = sqliteCipher.connect(self.detrans_sqlite_nome_execucao)
            cursor = conn.cursor()
            cursor.execute("PRAGMA key='senha_cifra'")

            self.progress = 3
            cria_db.criar(conn, cursor)

            self.progress = 4
            data_versao_bd = datetime.now()

            self.progress = 5
            if self.stopthread.isSet():
                raise ValueError('Geração detrans.sqlite cancelada, parada ao criar banco sqlite')

            self.progress = 6
            categoria.importa(conn, cursor, self.stopthread)
            self.progress = 7
            criacao_dados.importa(conn, cursor, self.stopthread)
            self.progress = 8
            cor.importa(conn, cursor, self.stopthread)
            self.progress = 9
            especie.importa(conn, cursor, self.stopthread)
            self.progress = 10
            lei.importa(conn, cursor, self.stopthread)
            self.progress = 11
            tipo_infracao.importa(conn, cursor, self.stopthread)
            self.progress = 13
            tipo_veiculo.importa(conn, cursor, self.stopthread)
            self.progress = 17
            uf_cidade.importa(conn, cursor, self.stopthread)
            self.progress = 18
            modelo.importa(conn, cursor, self.stopthread)
            self.progress = 20
            veiculo.importa(self, conn, cursor, self.stopthread)
            self.progress = 89
            agente.importa(conn, cursor, self.stopthread)
            self.progress = 91
            config_sinc.importa(conn, cursor, data_versao_bd, self.stopthread)
            self.progress = 94
            comprimir.comprimir_detrans_sqlite(self.detrans_sqlite_nome_execucao)
            self.progress = 99

            self.progress = 100

            if os.path.exists(self.detrans_sqlite_nome):
                os.remove(self.detrans_sqlite_nome)

            if os.path.exists(self.detrans_sqlite_nome + ".gz"):
                os.remove(self.detrans_sqlite_nome + ".gz")

            if os.path.exists(self.detrans_sqlite_nome_execucao + ".gz"):
                os.rename(self.detrans_sqlite_nome_execucao + ".gz",
                          self.detrans_sqlite_nome + ".gz")

            if os.path.exists(self.detrans_sqlite_nome_execucao):
                os.rename(self.detrans_sqlite_nome_execucao,
                          self.detrans_sqlite_nome)

            self.is_finalisado = True
            self.is_erro_processo = False
            self.is_cancelado = False
            self.detrans_sqlite.is_finished = True

        except Exception:
            self.is_finalisado = True
            self.is_erro_processo = True

        finally:
            self.is_finalisado = True
            self.detrans_sqlite.data_fim = datetime.now()
            self.detrans_sqlite.save()

    def stop(self):
        self.is_finalisado = False
        self.is_cancelado = True
        self.stopthread.set()

    def get_status_str(self):

        if self.is_cancelado:
            return 'Cancelado'

        if self.is_finalisado:
            return 'Concluido'

        return 'Processando'

    def get_status_mensagem_str(self):
        return self.progress


myProcess = None


class CriaSqliteView(View):
    template = 'detrans_sqlite/cria_sqlite.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        detrans_sqlite = Detrans_sqlite.objects.filter(is_finished=True).last()
        return render(request, self.template, {'sqlite': detrans_sqlite})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        global myProcess

        myProcess = ThreadDetransSqlite('importa')
        myProcess.start()

        return redirect('status-sqlite')


class CriaSqliteCanceladoView(View):
    template = 'detrans_sqlite/cria_sqlite_cancelado.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        return render(request, self.template)

    @method_decorator(permissao_geral_required())
    def post(self, request):
        global myProcess

        myProcess = ThreadDetransSqlite('importa')
        myProcess.start()

        return redirect('status-sqlite')


class StatusView(View):
    template = 'detrans_sqlite/status_sqlite.html'

    @method_decorator(permissao_geral_required())
    def get(self, request):
        global myProcess

        status = myProcess.get_status_str()
        erro = myProcess.is_erro_processo
        status_mensagem = myProcess.get_status_mensagem_str()
        if "refresh" in request.GET:
            import json
            list = json.dumps([status, erro, status_mensagem])
            return HttpResponse(list)
        return render(request, self.template, {'status': status,
                                               'erro': erro, 'status_mensagem': status_mensagem})

    @method_decorator(permissao_geral_required())
    def post(self, request):
        global myProcess

        myProcess.stop()

        return redirect('cria-sqlite-cancelado')
