# coding: utf-8
from django.db import connection


def importa(conn, cursor, data_versao_bd, stopthread):

    cursor_django = connection.cursor()
    cursor_django.execute('select distancia_captura_mov,horas_descarte,tempo_captura_mov from detransapp_configsinc')

    tupla_config_sinc = cursor_django.fetchall()

    print(tupla_config_sinc)
    cursor.executemany('INSERT INTO config_sinc (distancia_captura_mov,horas_descarte,tempo_captura_mov,data_sinc) values (?,?,?,?)',
                       [(float(tupla_config_sinc[0][0]),tupla_config_sinc[0][1],tupla_config_sinc[0][2],data_versao_bd)])
    conn.commit()

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Configuração"')