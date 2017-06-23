# coding: utf-8
from detransapp.models import Lei


def importa(conn, cursor, stopthread):

    leis = Lei.objects.all()

    tupla_leis = []

    for lei in leis:
        tupla_leis.append((lei.id, lei.lei))

    cursor.executemany("INSERT INTO lei VALUES (?,?)", tupla_leis)
    conn.commit()

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Lei"')