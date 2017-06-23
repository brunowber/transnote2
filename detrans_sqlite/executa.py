from detrans_sqlite.importa import *
import sqlite3
from detrans_sqlite import cria_db
from datetime import datetime
import os
import sys
from django.conf import settings


# noinspection PyArgumentList
def executa_importacao():

    try:

        os.remove('detrans.sqlite')

        conn = sqlite3.connect("detrans.sqlite")
        cursor = conn.cursor()

        cria_db.criar(conn, cursor)

        #TODO As consultas considerar data de alteracao
        data_versao_bd = datetime.now()

        categoria.importa(conn,cursor)
        cor.importa(conn,cursor)
        especie.importa(conn,cursor)
        lei.importa(conn,cursor)
        tipo_infracao.importa(conn,cursor)
        tipo_veiculo.importa(conn,cursor)
        uf_cidade.importa(conn,cursor)
        modelo.importa(conn,cursor)
        veiculo.importa(conn,cursor)
        agente.importa(conn,cursor)
        config_sinc.importa(conn,cursor,data_versao_bd)
        return True

    except:
        return False
