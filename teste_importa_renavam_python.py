import psycopg2
from itertools import izip_longest
import threading
from datetime import datetime
import json
import csv
import operator
import itertools


class ProprietarioImporta():
    def __init__(self, documento, nome):
        self.documento = documento
        self.nome = nome

    def __eq__(self, other):
        if other:
            return (self.documento == other.documento and self.nome == other.nome)
        return False


conn_string = "host='localhost' dbname='detrans6' user='postgres' password='root'"

connection = psycopg2.connect(conn_string)
count = 0


def importa_veiculos(veiculos):
    if veiculos[0][0] == 'chassi':
        veiculos.remove(veiculos[0])

    # fieldnames = ['chassi','renavam', 'placa', 'modelo','cor','tipo_veiculo','especie','categoria','municipio',
    #          'ano_fabricacao','ano_modelo','nr_passageiros','nr_motor','proprietario']

    insert_veiculo = '''INSERT INTO detransapp_veiculo (chassi, renavam,placa, modelo_id,cor_id, tipo_veiculo_id,
    especie_id, categoria_id,cidade_id, ano_fabricacao, ano_modelo, num_passageiro, nr_motor, data, data_alterado) values
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())'''

    erros_importa_veiculo = []
    cur = connection.cursor()

    try:
        cur.executemany(insert_veiculo, veiculos)
        connection.commit()
    except Exception as e:
        connection.rollback()

        for insert_item in veiculos:
            try:
                cur.executemany(insert_veiculo, [insert_item])
                connection.commit()
            except Exception as ex:
                connection.rollback()

                erros_importa_veiculo.append(
                    {'erro': 'insert_veiculo', 'ex': '%s ; %s' % (type(ex), ex), 'item': insert_item})
    cur.close()

    return erros_importa_veiculo


def importa_veiculos_csv(veiculos):
    if veiculos[0][0] == 'chassi':
        veiculos.remove(veiculos[0])

    # fieldnames = ['chassi','renavam', 'placa', 'modelo','cor','tipo_veiculo','especie','categoria','municipio',
    #          'ano_fabricacao','ano_modelo','nr_passageiros','nr_motor','proprietario']

    insert_veiculo = '''INSERT INTO veiculo_csv (chassi, renavam,placa, modelo,cor, tipo_veiculo,
    especie, categoria,municipio, ano_fabricacao, ano_modelo, num_passageiro, nr_motor, proprietario, nome_proprietario) values
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    erros_importa_veiculo = []
    cur = connection.cursor()

    try:
        cur.executemany(insert_veiculo, veiculos)
        connection.commit()
    except Exception as e:
        connection.rollback()

        for insert_item in veiculos:
            try:
                cur.executemany(insert_veiculo, [insert_item])
                connection.commit()
            except Exception as ex:
                connection.rollback()

                erros_importa_veiculo.append(
                    {'erro': 'insert_veiculo', 'ex': '%s ; %s' % (type(ex), ex), 'item': insert_item})
    cur.close()

    return erros_importa_veiculo


def importa_veiculo_proprietario(veiculo_proprietario_list):
    if veiculo_proprietario_list[0][0] == 'chassi':
        veiculo_proprietario_list.remove(veiculo_proprietario_list[0])

    insert_veiculo_proprietario = '''INSERT INTO detransapp_veiculoproprietario (veiculo_id, proprietario_id, data) values (%s, %s, now())'''

    erros_importa_veiculo_proprietario = []
    cur = connection.cursor()

    try:
        cur.executemany(insert_veiculo_proprietario, veiculo_proprietario_list)
        connection.commit()
    except Exception as e:
        connection.rollback()

        for insert_item in veiculo_proprietario_list:
            try:
                cur.executemany(insert_veiculo_proprietario, [insert_item])
                connection.commit()
            except Exception as ex:
                connection.rollback()

                erros_importa_veiculo_proprietario.append(
                    {'erro': 'insert_veiculo_proprietario', 'ex': '%s ; %s' % (type(ex), ex), 'item': insert_item})
    cur.close()

    return erros_importa_veiculo_proprietario


class ImportaRenavamThread(threading.Thread):
    def __init__(self, next_n_lines):
        threading.Thread.__init__(self)
        self.next_n_lines = next_n_lines

    def run(self):
        for linha in self.next_n_lines:

            if linha is None or linha.strip() == '':
                continue

            '''try:
                importa_renavam(linha.strip())
            except:
                continue
            '''
        print str(datetime.now())


'''
10:54
11:00 100.000

11:03
11:09 140.153

11:10
11:16 170.000

11:41
11:56 447317

12:29
12:44 458072
'''

''' Total linhas do arquivo renavam = '4.465.590'
    101.159 em 15 minutos com infinitas Threads, com processador em 100 %, com o tempo o numero insercoes diminui no banco
    167.856 em 15 minutos com 4 Threads, com processador oscilando em 80%, 167.856 X 27 = 4.532.112, 15 min X 27
    167.856 em 15 minutos com 4 Threads, com processador oscilando em 80%, 187.317 X 25 = 4.682.925, 15 min X 25 estimativa de 6,25 horas
    193.351 em 15 minutos com 4 Threads, com processador oscilando em ??, 193.351 X 24 = 4.640.424, 15 min X 24 estimativa de 6 horas
'''


def teste3_utilzando_threads():
    arq = open('detrans_txt/Renavam.txt', 'r')

    '''
        Total de linhas 4.465.590 / 4 = 1.116.397,5 , arendondado para 1.116.400 linhas por Threads genrando um total de 4 Threads.

    '''
    numero_linhas = 1116400
    print 'Inicio ', datetime.now()

    with arq as f:

        myThreads = []

        for next_n_lines in izip_longest(*[f] * numero_linhas):
            myThreads.append(ImportaRenavamThread(next_n_lines))

        for tr in myThreads:
            tr.start()


''' Total linhas do arquivo renavam = '4.465.590'
    97.113 em 15 minutos, performace pessima
    387.131 11:55:47  as 12:55
    4.447.864 20:57 as 22:16 tem renavam duplicado'''


def teste4_sem_thread():
    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Inicio ', datetime.now()

    numero_linhas = 5000

    linhas_problematicas = []

    with arq as f:
        '''for next_n_lines in izip_longest(*[f] * numero_linhas):

            linhas_problematicas.extend(importa_renavam(next_n_lines))'''

    print 'Fim ', datetime.now()
    print 'Linhas problematicas'
    print linhas_problematicas


def count_renavam_txt():
    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Count linhas renavam txt : ', len(arq.readlines())


def count_renavam_csv():
    arq = open('renavam.csv', 'r')
    print 'Count linhas renavam csv : ', (len(arq.readlines()) - 1)


def exporta_renavam_csv():
    fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
                  'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario', 'nome_proprietario']

    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Inicio ', datetime.now()

    linhas_problematicas = []

    with open('renavam.csv', 'w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for linha in arq.readlines():

            if linha is None or linha.strip() == '':
                continue
            try:
                linha = unicode(linha.strip())

                chassi_veiculo = linha[122:143].strip()
                renavam_veiculo = linha[26:37].strip()
                placa_veiculo = linha[0:7].strip()
                modelo_veiculo = int(linha[7:13])
                cor_veiculo = int(linha[13:15])
                tipo_veiculo = int(linha[15:17])
                especie_veiculo = int(linha[17:19])
                categoria_veiculo = int(linha[19:21])
                municipio_veiculo = linha[21:26]

                ano_fabricacao_veiculo = int(linha[37:41])
                ano_modelo_veiculo = int(linha[41:45])
                num_passageiros_veiculo = linha[119:122]
                nr_motor_veiculo = linha[143:164].strip()
                cpf_proprietario = linha[45:59].strip()
                nome_proprietario = linha[59:119].strip()

                writer.writerow({'chassi': chassi_veiculo, 'renavam': renavam_veiculo, 'placa': placa_veiculo,
                                 'modelo': modelo_veiculo, 'cor': cor_veiculo, 'tipo_veiculo': tipo_veiculo,
                                 'especie': especie_veiculo, 'categoria': categoria_veiculo,
                                 'municipio': municipio_veiculo,
                                 'ano_fabricacao': ano_fabricacao_veiculo, 'ano_modelo': ano_modelo_veiculo,
                                 'nr_passageiros': num_passageiros_veiculo, 'nr_motor': nr_motor_veiculo,
                                 'proprietario': cpf_proprietario, 'nome_proprietario': nome_proprietario})

            except Exception as e:
                linhas_problematicas.append({'erro': 'unicode', 'ex': '%s ; %s' % (type(e), e), 'linha': linha})
                continue

    print 'Fim ', datetime.now()


def remove_linhas_duplicadas_renavam_csv():
    linhas = open('renavam.csv').readlines()
    print 'Count : ', len(linhas)
    uniqlines = set(linhas)
    print 'Count 2 : ', len(uniqlines)
    bar = open('renavam2.csv', 'w')

    uniqlines = set(uniqlines)

    bar.writelines(uniqlines)

    bar.close()


def renavam_csv_final():
    fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
                  'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario', 'nome_proprietario']
    print 'Inicio : ', str(datetime.now())

    documentos = []

    documentos_gravados = []

    prop3_csv = open('renavam3.csv', 'w')

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=fieldnames, delimiter=';')
    prop3_writer.writeheader()

    with open('renavam2.csv', 'rb') as csvfile:
        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        # sortedlist = sorted(dict_render, key=operator.itemgetter('chassi'), reverse=False)

        # list(filter(lambda x: x[0] not in sortedlist, sortedlist))
        # nova_lista = interador(sortedlist)
        # nova_lista = list(nova_lista)

        for group, line in itertools.groupby(dict_render, key=lambda x: x['chassi']):
            itens = list(line)
            prop3_writer.writerow(itens[0])

    prop3_csv.close()

    print 'Fim : ', str(datetime.now())


def renavam_csv_ordenado():
    fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
                  'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario', 'nome_proprietario']
    print 'Inicio : ', str(datetime.now())

    documentos = []

    documentos_gravados = []

    prop3_csv = open('renavam_ordenado.csv', 'w')

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=fieldnames, delimiter=';')
    prop3_writer.writeheader()

    with open('renavam.csv', 'rb') as csvfile:
        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')
        sortedlist = sorted(dict_render, key=operator.itemgetter('chassi'), reverse=False)

        # list(filter(lambda x: x[0] not in sortedlist, sortedlist))
        # nova_lista = interador(sortedlist)
        # nova_lista = list(nova_lista)

        for linha in sortedlist:
            prop3_writer.writerow(linha)

        '''for group, line in itertools.groupby(sortedlist, key=lambda x: x['chassi']):
            itens = list(line)
            prop3_writer.writerow(itens[0])'''

    prop3_csv.close()

    print 'Fim : ', str(datetime.now())


def renavam_csv_exporta_veiculo_bd():
    fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
                  'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario', 'nome_proprietario']
    print 'Inicio : ', str(datetime.now())

    print 'Inserindo veiculos ...'
    print 'Inicio ', datetime.now()
    numero_linhas = 100000

    with open('renavam.csv', 'rb') as csvfile:
        dict_render = csv.reader(csvfile, delimiter=';')

        erros_veiculo = []

        for pagina in izip_longest(*[dict_render] * numero_linhas):

            list_pagina = list(pagina)

            try:
                veiculos = [tuple((line[0], line[1], line[2], line[3], line[4],
                                   line[5], line[6], line[7],
                                   line[8], line[9], line[10],
                                   line[11], line[12], line[13], line[14])) for line in list_pagina]
            except:

                veiculos = []

                for line in list_pagina:
                    if line is None:
                        continue

                    veiculos.append((line[0], line[1], line[2], line[3], line[4],
                                     line[5], line[6], line[7], line[8], line[9],
                                     line[10], line[11], line[12], line[13], line[14]))

            erros_veiculo.extend(importa_veiculos_csv(veiculos))

    print 'Erros veiculos : ', len(erros_veiculo)

    for erro_veiculo in erros_veiculo:
        print erro_veiculo

    print 'Fim : ', str(datetime.now())


def renavam_csv_chassis_duplicados():
    fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
                  'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario', 'nome_proprietario']
    print 'Inicio : ', str(datetime.now())

    documentos = []

    documentos_gravados = []

    prop3_csv = open('renavam_chassis_duplicados2.csv', 'w')

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=fieldnames, delimiter=';')
    prop3_writer.writeheader()

    with open('renavam2.csv', 'rb') as csvfile:

        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        # sortedlist = sorted(dict_render, key=operator.itemgetter('chassi'), reverse=False)

        # list(filter(lambda x: x[0] not in sortedlist, sortedlist))
        # nova_lista = interador(sortedlist)
        # nova_lista = list(nova_lista)

        for group, line in itertools.groupby(dict_render, key=lambda x: x['chassi']):
            itens = list(line)

            if len(itens) > 1:
                print 'Encontro'
                break


    prop3_csv.close()

    print 'Fim : ', str(datetime.now())


fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
              'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario']


def exporta_veiculos_csv():
    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Inicio ', datetime.now()

    linhas_problematicas = []

    with open('veiculos.csv', 'w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for linha in arq.readlines():

            if linha is None or linha.strip() == '':
                continue
            try:
                linha = unicode(linha.strip())

                chassi_veiculo = linha[122:143].strip()
                renavam_veiculo = linha[26:37].strip()
                placa_veiculo = linha[0:7].strip()
                modelo_veiculo = int(linha[7:13])
                cor_veiculo = int(linha[13:15])
                tipo_veiculo = int(linha[15:17])
                especie_veiculo = int(linha[17:19])
                categoria_veiculo = int(linha[19:21])
                municipio_veiculo = linha[21:26]

                ano_fabricacao_veiculo = int(linha[37:41])
                ano_modelo_veiculo = int(linha[41:45])
                num_passageiros_veiculo = linha[119:122]
                nr_motor_veiculo = linha[143:164].strip()
                cpf_proprietario = linha[45:59].strip()

                writer.writerow({'chassi': chassi_veiculo,
                                 'modelo': modelo_veiculo, 'cor': cor_veiculo,
                                 'especie': especie_veiculo,
                                 'ano_fabricacao': ano_fabricacao_veiculo})

            except Exception as e:
                linhas_problematicas.append({'erro': 'unicode', 'ex': '%s ; %s' % (type(e), e), 'linha': linha})
                continue

    print 'Fim ', datetime.now()


def exporta_veiculos_proprietario_csv():
    fieldnames_renavam = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria',
                          'municipio',
                          'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario',
                          'nome_proprietario']

    arq = open('renavam3.csv', 'r')

    dict_render = csv.DictReader(arq, fieldnames=fieldnames_renavam, delimiter=';')

    print 'Inicio ', datetime.now()

    linhas_problematicas = []

    with open('veiculos_proprietario.csv', 'w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=['chassi', 'proprietario'], delimiter=';')

        writer.writeheader()
        for linha in dict_render:

            try:

                chassi_veiculo = linha['chassi']
                cpf_proprietario = linha['proprietario']

                writer.writerow({'chassi': chassi_veiculo, 'proprietario': cpf_proprietario})

            except Exception as e:
                linhas_problematicas.append({'erro': 'unicode', 'ex': '%s ; %s' % (type(e), e), 'linha': linha})
                continue

    print 'Fim ', datetime.now()


def remove_linhas_duplicadas_veiculo():
    linhas = open('veiculos.csv').readlines()
    print 'Count : ', len(linhas)
    uniqlines = set(linhas)
    print 'Count 2 : ', len(uniqlines)
    bar = open('veiculos2.csv', 'w')

    uniqlines = set(uniqlines)

    bar.writelines(uniqlines)

    bar.close()


def remove_linhas_duplicadas_veiculos_proprietario():
    linhas = open('veiculos_proprietario.csv').readlines()
    print 'Count : ', len(linhas)
    uniqlines = set(linhas)
    print 'Count 2 : ', len(uniqlines)
    bar = open('veiculos_proprietario2.csv', 'w')

    uniqlines = set(uniqlines)

    bar.writelines(uniqlines)

    bar.close()


def proprietarios_csv_final():
    print 'Inicio : ', str(datetime.now())

    documentos = []

    documentos_gravados = []

    prop3_csv = open('veiculos3.csv', 'w')
    fieldnames = ['documento', 'nome']

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=['documento', 'nome'], delimiter=';')
    prop3_writer.writeheader()

    with open('veiculos2.csv', 'rb') as csvfile:
        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        sortedlist = sorted(dict_render, key=operator.itemgetter('documento'), reverse=False)

        # list(filter(lambda x: x[0] not in sortedlist, sortedlist))
        # nova_lista = interador(sortedlist)
        # nova_lista = list(nova_lista)

        for group, line in itertools.groupby(sortedlist, key=lambda x: x['documento']):
            itens = list(line)
            prop3_writer.writerow(itens[0])

    prop3_csv.close()

    print 'Fim : ', str(datetime.now())


'''
Cpf duplicado

[{'nome': 'PEDRO LUIZ MARTINS', 'documento': '00053459059915'}, {'nome': 'ZELIA MARTINS MENDES', 'documento': '00053459059915'}]
'''


def importa_renavam_csv_veiculo_proprietario():
    print 'Inserindo veiculos ...'
    print 'Inicio ', datetime.now()
    numero_linhas = 5000

    with open('renavam3.csv', 'rb') as csvfile:
        dict_render = csv.reader(csvfile, delimiter=';')

        erros_veiculo = []

        for pagina in izip_longest(*[dict_render] * numero_linhas):

            list_pagina = list(pagina)

            try:
                veiculos = [tuple((line[0], line[1], line[2], line[3], line[4],
                                   line[5], line[6], line[7],
                                   line[8], line[9], line[10],
                                   line[11], line[12])) for line in list_pagina]
            except:

                veiculos = []

                for line in list_pagina:
                    if line is None:
                        continue

                    veiculos.append((line[0], line[1], line[2], line[3], line[4],
                                     line[5], line[6], line[7], line[8], line[9],
                                     line[10], line[11], line[12]))

            erros_veiculo.extend(importa_veiculos(veiculos))

    print 'Erros veiculos : ', len(erros_veiculo)

    for erro_veiculo in erros_veiculo:
        print erro_veiculo

    print 'Fim ', datetime.now()
    print 'Inicio ', datetime.now()

    erros_veiculo_proprietario = []
    print 'Vinculando proprietario ao veiculo ...'
    with open('veiculos_proprietario3.csv', 'rb') as csvfile:
        dict_render = csv.reader(csvfile, delimiter=';')

        for pagina in izip_longest(*[dict_render] * numero_linhas):

            list_pagina = list(pagina)
            try:
                veiculo_proprietario = [tuple((line[0], line[1])) for line in list_pagina]
            except Exception as ex:
                veiculo_proprietario = []

                for line in list_pagina:
                    if line is None:
                        continue

                    veiculo_proprietario.append((line[0], line[1]))

            erros_veiculo_proprietario.extend(importa_veiculo_proprietario(veiculo_proprietario))

    print 'Erros veiculo proprietario : ', len(erros_veiculo_proprietario)

    for erro_veiculo_proprietario in erros_veiculo_proprietario:
        print erro_veiculo_proprietario

    # del veiculo_proprietario
    print 'Fim ', datetime.now()


def veiculos_csv_final():
    print 'Inicio : ', str(datetime.now())

    prop3_csv = open('veiculos3.csv', 'w')

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=fieldnames, delimiter=';')
    prop3_writer.writeheader()

    with open('veiculos2.csv', 'rb') as csvfile:
        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        for group, line in itertools.groupby(dict_render, key=lambda x: x['chassi']):
            itens = list(line)
            prop3_writer.writerow(itens[0])

    prop3_csv.close()

    print 'Fim : ', str(datetime.now())


def veiculos_proprietario_csv_final():
    print 'Inicio : ', str(datetime.now())

    prop3_csv = open('veiculos_proprietario3.csv', 'w')

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=fieldnames, delimiter=';')
    prop3_writer.writeheader()

    with open('veiculos_proprietario2.csv', 'rb') as csvfile:
        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        for group, line in itertools.groupby(dict_render, key=lambda x: x['chassi']):
            itens = list(line)
            prop3_writer.writerow(itens[0])

    prop3_csv.close()

    print 'Fim : ', str(datetime.now())


def executa_importacao_veiculo():
    print 'CSV exporta veiculos_propritario'
    exporta_veiculos_proprietario_csv()
    print 'CSV remove linhas veiculos_propritario'
    remove_linhas_duplicadas_veiculos_proprietario()

    print 'CSV remove chassi duplicado veiculos_propritario'
    veiculos_proprietario_csv_final()

    importa_renavam_csv_veiculo_proprietario()


def teste_unicode_linha():
    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Inicio ', datetime.now()

    linhas_erros = []

    for linha in arq.readlines():

        try:
            unicode(linha)
        except:
            linhas_erros.append(linha)

    print 'Total linhas codificacao invalida : ', len(linhas_erros)

    for erro in linhas_erros:
        print erro.strip()


def teste_chassi_duplicado(chassi):
    print 'Inicio ', datetime.now()

    with open('renavam3.csv', 'rb') as csvfile:

        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        for linha in dict_render:

            if chassi in linha['chassi']:
                print linha

    print 'Fim ', datetime.now()


'''
if __name__ == '__main__':

    executa_importacao_veiculo()'''
