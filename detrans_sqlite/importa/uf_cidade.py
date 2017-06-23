# coding: utf-8
from detransapp.models import Cidade, UF


def importa(conn, cursor, stopthread):

    ufs = UF.objects.get_ufs_sicronismo()

    tupla_ufs = []

    for uf in ufs:
        tupla_ufs.append((uf.id, uf.sigla, uf.nome))

    cursor.executemany("INSERT INTO uf VALUES (?,?,?)", tupla_ufs)
    conn.commit()

    for uf in ufs:

        cidades = Cidade.objects.get_cidades_sicronismo(uf.id)

        tupla_cidades = []

        for cidade in cidades:
            tupla_cidades.append((cidade.codigo, cidade.nome, cidade.uf_id))

        cursor.executemany("INSERT INTO cidade (codigo,nome,uf_id) VALUES (?,?,?)", tupla_cidades)
        conn.commit()

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "UF - Cidade"')