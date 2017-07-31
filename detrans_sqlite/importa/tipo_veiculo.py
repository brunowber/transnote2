# coding: utf-8
from detransapp.models import TipoVeiculo


def importa(conn, cursor, stopthread):

    tipos_veiculo = TipoVeiculo.objects.get_tipos_veiculo_sicronismo()

    tupla_tipos_veiculo = []

    for tipo_veiculo in tipos_veiculo:
        tupla_tipos_veiculo.append((tipo_veiculo.codigo, tipo_veiculo.descricao))

    cursor.executemany("INSERT INTO tipo_veiculo VALUES (?,?)", tupla_tipos_veiculo)
    conn.commit()

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Veiculo"')