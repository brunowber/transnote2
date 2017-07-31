import sqlite3
from datetime import datetime

from detrans_sqlite import cria_db

conn = sqlite3.connect("detrans.sqlite")
cursor = conn.cursor()

cria_db.criar(conn, cursor)



# TODO As consultas considerar data de alteracao
data_versao_bd = datetime.now()

print 'Inicio : ', data_versao_bd

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.join(BASE_DIR, 'detrans')

import sys

sys.path += [BASE_DIR]
os.environ['DJANGO_SETTINGS_MODULE'] = 'detrans.settings.vilmar'

from detransapp.models import Categoria, Cor, Especie, TipoInfracao, TipoVeiculo, Cidade, UF, Modelo, Veiculo, Lei
from django.db import connection

categorias = Categoria.objects.get_categorias_sicronismo()

tupla_categorias = []

for categoria in categorias:
    tupla_categorias.append((categoria.codigo, categoria.descricao))

cursor.executemany("INSERT INTO categoria VALUES (?,?)", tupla_categorias)
conn.commit()

cores = Cor.objects.get_cores_sicronismo()

tupla_cores = []

for cor in cores:
    tupla_cores.append((cor.codigo, cor.descricao))

cursor.executemany("INSERT INTO cor VALUES (?,?)", tupla_cores)
conn.commit()

especies = Especie.objects.get_especies_sicronismo()

tupla_especies = []

for especie in especies:
    tupla_especies.append((especie.codigo, especie.descricao))

cursor.executemany("INSERT INTO especie VALUES (?,?)", tupla_especies)
conn.commit()

# TODO Verificar as ligacoes
leis = Lei.objects.all()

tupla_leis = []

for lei in leis:
    tupla_leis.append((lei.id, lei.lei))

cursor.executemany("INSERT INTO lei VALUES (?,?)", tupla_leis)
conn.commit()

tipos_infracao = TipoInfracao.objects.get_tipos_infracao_sicronismo(1)
num_pages = tipos_infracao.paginator.num_pages
count = 1

while True:

    tupla_tipos_infracao = []

    for tipo_infracao in tipos_infracao:
        tupla_tipos_infracao.append((tipo_infracao.codigo, tipo_infracao.descricao, tipo_infracao.lei_id,
                                     tipo_infracao.is_condutor_obrigatorio, tipo_infracao.ativo))

    cursor.executemany("INSERT INTO tipo_infracao VALUES (?,?,?,?,?)", tupla_tipos_infracao)
    conn.commit()
    count += 1

    if count > num_pages:
        break

    tipos_infracao = TipoInfracao.objects.get_modelos_sicronismo(count)

tipos_veiculo = TipoVeiculo.objects.get_tipos_veiculo_sicronismo()

tupla_tipos_veiculo = []

for tipo_veiculo in tipos_veiculo:
    tupla_tipos_veiculo.append((tipo_veiculo.codigo, tipo_veiculo.descricao))

cursor.executemany("INSERT INTO tipo_veiculo VALUES (?,?)", tupla_tipos_veiculo)
conn.commit()

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

veiculos = Veiculo.objects.get_veiculos_sicronismo(1)
num_pages = veiculos.paginator.num_pages
count = 1

while True:

    tupla_veiculos = []

    for veiculo in veiculos:
        tupla_veiculos.append((veiculo.renavam,
                               veiculo.chassi,
                               veiculo.nr_motor,
                               veiculo.placa,
                               veiculo.modelo_id,
                               veiculo.tipo_veiculo_id,
                               veiculo.especie_id,
                               veiculo.cidade_id,
                               veiculo.cor_id,
                               veiculo.categoria_id,
                               veiculo.ano_fabricacao,
                               veiculo.ano_modelo,
                               veiculo.num_passageiro,
                               veiculo.cidade_id))

    cursor.executemany("INSERT INTO veiculo (renavam, chassi, nr_motor, placa, modelo_codigo, tipo_veiculo_codigo, "
                       "especie_codigo, cidade_codigo, cor_codigo, categoria_codigo, ano_fabricacao, ano_modelo,"
                       "num_passageiro, cidade_codigo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tupla_veiculos)
    conn.commit()

    count += 1

    if count > num_pages:
        break

    veiculos = Veiculo.objects.get_veiculos_sicronismo(count)

cursor.execute("CREATE INDEX veiculo_placa_index ON veiculo(placa);")
conn.commit()

cursor_django = connection.cursor()

cursor_django.execute(
    'select a.user_ptr_id as id,a.identificacao as identificacao,b.first_name as first_name,b.last_name as last_name,'
    'b.username as username,b.password as password '
    # ', a.data as data,a.data_alterado as data_alterado '
    'from detransapp_agente a '
    'inner join auth_user b on (a.user_ptr_id=b.id) where b.is_active=true')

tupla_agentes = cursor_django.fetchall()

cursor.executemany(
    'INSERT INTO agente (id, identificacao, first_name, last_name, username, password) values (?,?,?,?,?,?)',
    tupla_agentes)
conn.commit()

cursor_django.execute('select distancia_captura_mov,horas_descarte,tempo_captura_mov from detransapp_configsinc')

tupla_config_sinc = cursor_django.fetchall()

cursor.executemany(
    'INSERT INTO config_sinc (distancia_captura_mov,horas_descarte,tempo_captura_mov,data_sinc) values (?,?,?,?)',
    [(float(tupla_config_sinc[0][0]), tupla_config_sinc[0][1], tupla_config_sinc[0][2], data_versao_bd)])
conn.commit()

print 'Fim : ', datetime.now()
