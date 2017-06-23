# coding: utf-8
from django.db import connection


def importa(conn, cursor, stopthread):

    cursor_django = connection.cursor()

    cursor_django.execute('select a.user_ptr_id as id,a.identificacao as identificacao,b.first_name as first_name,b.last_name as last_name,'
                          'b.username as username,b.password as password '
                          #', a.data as data,a.data_alterado as data_alterado '
                          'from detransapp_agente a '
                          'inner join auth_user b on (a.user_ptr_id=b.id) where b.is_active=true')

    tupla_agentes = cursor_django.fetchall()

    cursor.executemany('INSERT INTO agente (id, identificacao, first_name, last_name, username, password) values (?,?,?,?,?,?)',tupla_agentes)
    conn.commit()

    if stopthread.isSet():
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Agente"')