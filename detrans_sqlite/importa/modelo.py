# coding: utf-8
from detransapp.models import Modelo


def importa(conn, cursor, stopthread):

    modelos = Modelo.objects.get_modelos_sicronismo(1)
    num_pages = modelos.paginator.num_pages
    count = 1

    while True:

        tupla_modelos = []

        for modelo in modelos:
            tupla_modelos.append((modelo.codigo, modelo.descricao))

        cursor.executemany("INSERT INTO modelo VALUES (?,?)", tupla_modelos)
        conn.commit()

        count += 1

        if count > num_pages:
            break

        modelos = Modelo.objects.get_modelos_sicronismo(count)

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Modelo"')