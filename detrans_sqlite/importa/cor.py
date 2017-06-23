# coding: utf-8
from detransapp.models import Cor


def importa(conn, cursor, stopthread):

    cores = Cor.objects.get_cores_sicronismo()
    tupla_cores = []

    for cor in cores:
        tupla_cores.append((cor.codigo, cor.descricao))

    cursor.executemany("INSERT INTO cor VALUES (?,?)", tupla_cores)
    conn.commit()
    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Cor"')