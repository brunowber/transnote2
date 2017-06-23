# coding: utf-8
from detransapp.models import TipoInfracao


def importa(conn, cursor, stopthread):

    tipos_infracao = TipoInfracao.objects.get_tipos_infracao_sicronismo(1)
    num_pages = tipos_infracao.paginator.num_pages
    count = 1

    while True:

        tupla_tipos_infracao = []

        for tipo_infracao in tipos_infracao:
            tupla_tipos_infracao.append((tipo_infracao.codigo, tipo_infracao.descricao, tipo_infracao.lei_id, tipo_infracao.is_condutor_obrigatorio,tipo_infracao.ativo))

        cursor.executemany("INSERT INTO tipo_infracao VALUES (?,?,?,?,?)", tupla_tipos_infracao)
        conn.commit()
        count += 1

        if count > num_pages:
            break

        tipos_infracao = TipoInfracao.objects.get_modelos_sicronismo(count)

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Tipo infração"')