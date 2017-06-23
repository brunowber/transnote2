import psycopg2
from itertools import izip_longest
from datetime import datetime
import csv
import operator
import itertools

conn_string = "host='localhost' dbname='detrans6' user='postgres' password='root'"
connection = psycopg2.connect(conn_string)


def exporta_proprietarios_csv():
    fieldnames_renavam = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria',
                          'municipio',
                          'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario',
                          'nome_proprietario']

    arq = open('renavam3.csv', 'r')
    print 'Inicio ', datetime.now()

    dict_render = csv.DictReader(arq, fieldnames=fieldnames_renavam, delimiter=';')

    linhas_problematicas = []

    with open('proprietarios.csv', 'w') as csvfile:
        fieldnames = ['documento', 'nome']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for linha in dict_render:

            try:
                cpf_proprietario = linha['proprietario']
                nome_proprietario = linha['nome_proprietario']

                writer.writerow({'documento': cpf_proprietario, 'nome': nome_proprietario})

            except Exception as e:
                linhas_problematicas.append({'erro': 'unicode', 'ex': '%s ; %s' % (type(e), e), 'linha': linha})
                continue

    print 'Fim ', datetime.now()


def remove_linhas_duplicadas_proprietario():
    print 'Inicio : ', str(datetime.now())
    linhas = open('proprietarios.csv').readlines()
    print 'Count : ', len(linhas)
    uniqlines = set(linhas)
    print 'Count 2 : ', len(uniqlines)
    bar = open('proprietarios2.csv', 'w')

    uniqlines = set(uniqlines)
    bar.writelines(uniqlines)

    bar.close()
    print 'Fim : ', str(datetime.now())


def proprietarios_csv_final():
    print 'Inicio : ', str(datetime.now())

    prop3_csv = open('proprietarios3.csv', 'w')
    fieldnames = ['documento', 'nome']

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=['documento', 'nome'], delimiter=';')
    prop3_writer.writeheader()

    with open('proprietarios2.csv', 'rb') as csvfile:
        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        sortedlist = sorted(dict_render, key=operator.itemgetter('documento'), reverse=False)

        for group, line in itertools.groupby(sortedlist, key=lambda x: x['documento']):
            itens = list(line)
            prop3_writer.writerow(itens[0])

    prop3_csv.close()

    print 'Fim : ', str(datetime.now())


def importa_proprietarios(proprietarios):
    if proprietarios[0][0] == 'documento':
        proprietarios.remove(proprietarios[0])

    erros_importa_proprietario = []
    cur = connection.cursor()

    insert_proprietario = '''INSERT INTO detransapp_proprietario (documento, nome) values (%s, %s)'''

    try:
        cur.executemany(insert_proprietario, proprietarios)
        connection.commit()
    except Exception as e:
        connection.rollback()

        for insert_item in proprietarios:
            try:
                cur.executemany(insert_proprietario, [insert_item])
                connection.commit()
            except Exception as ex:
                connection.rollback()

                erros_importa_proprietario.append(
                    {'erro': 'insert_proprietario', 'ex': '%s ; %s' % (type(ex), ex), 'item': insert_item})
    cur.close()

    return erros_importa_proprietario


'''
Cpf duplicado

[{'nome': 'PEDRO LUIZ MARTINS', 'documento': '00053459059915'}, {'nome': 'ZELIA MARTINS MENDES', 'documento': '00053459059915'}]
'''


def importa_renavam_csv_proprietario():
    print 'Inicio ', datetime.now()
    numero_linhas = 10000

    erros_proprietario = []

    with open('proprietarios3.csv', 'rb') as csvfile:
        # fieldnames = ['documento', 'nome']
        dict_render = csv.reader(csvfile, delimiter=';')

        for pagina in izip_longest(*[dict_render] * numero_linhas):

            list_pagina = list(pagina)

            try:
                veiculos = [tuple((line[0], line[1])) for line in list_pagina]
            except:

                veiculos = []

                for line in list_pagina:
                    if line is None:
                        continue

                    veiculos.append((line[0], line[1]))

            erros_proprietario.extend(importa_proprietarios(veiculos))
    print 'Fim ', datetime.now()
    return erros_proprietario


def executa_importacao_proprietario():
    print 'CSV exporta proprietarios'
    exporta_proprietarios_csv()
    print 'CSV remove linhas duplicadas proprietarios'
    remove_linhas_duplicadas_proprietario()
    print 'CSV remove documentos duplicados proprietarios'
    proprietarios_csv_final()

    print 'Inserindo proprietarios ...'
    for erro in importa_renavam_csv_proprietario():
        print erro


'''if __name__ == '__main__':

    executa_importacao_proprietario()'''
