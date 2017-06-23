# coding: utf-8
from detransapp.models import Categoria


def importa(conn, cursor, stopthread):

    categorias = Categoria.objects.get_categorias_sicronismo()

    tupla_categorias = []

    for categoria in categorias:
        tupla_categorias.append((categoria.codigo, categoria.descricao))

    cursor.executemany("INSERT INTO categoria VALUES (?,?)", tupla_categorias)
    conn.commit()

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Categoria"')