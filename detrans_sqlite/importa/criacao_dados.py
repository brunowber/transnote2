# coding: utf-8
import datetime

from detransapp.models import Detrans_sqlite


def importa(conn, cursor, stopthread):
    try:
        detrans_sqlite = Detrans_sqlite.objects.filter(is_finished=True).last()
        data = detrans_sqlite.data_fim
        tupla_dados = [int(detrans_sqlite.id), str(data)[0:19]]
    except:
        id = Detrans_sqlite.objects.latest('id')
        data = Detrans_sqlite.objects.latest('id').data_versao
        tupla_dados = [int(id.id), str(data)[0:19]]

    cursor.execute('INSERT INTO dados_sqlite (id, data_versao) values (?,?)', tupla_dados)
    print 'executa'
    conn.commit()
    print "terminou"

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Data de criação do banco móvel"')