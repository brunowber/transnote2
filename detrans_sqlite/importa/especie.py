# coding: utf-8
from detransapp.models import Especie


def importa(conn, cursor, stopthread):

    especies = Especie.objects.get_especies_sicronismo()

    tupla_especies = []

    for especie in especies:
        tupla_especies.append((especie.codigo, especie.descricao))

    cursor.executemany("INSERT INTO especie VALUES (?,?)", tupla_especies)
    conn.commit()

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Especie"')