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


conn_string = "host='localhost' dbname='detrans5' user='postgres' password='root'"

connection = psycopg2.connect(conn_string)
count = 0


# TODO Existe renavam duplicado ERRO
# TODO Remover cidade_id manter cidade_codigo
def importa_renavam(linhas):
    linhas_problematicas = []

    proprietarios = []

    veiculos_tupla = []
    proprietarios_tupla = []

    veiculos_proprietarios_tupla = []

    for linha in linhas:

        if linha is None or linha.strip() == '':
            continue

        try:
            linha = unicode(linha.strip())

            placa_veiculo = linha[0:7].strip()
            modelo_veiculo = int(linha[7:13])
            cor_veiculo = int(linha[13:15])
            tipo_veiculo = int(linha[15:17])
            especie_veiculo = int(linha[17:19])
            categoria_veiculo = int(linha[19:21])
            municipio_veiculo = linha[21:26]
            renavam_veiculo = linha[26:37].strip()
            ano_fabricacao_veiculo = int(linha[37:41])
            ano_modelo_veiculo = int(linha[41:45])

            cpf_proprietario = linha[45:59].strip()

            nome_proprietario = linha[59:119].strip()
            num_passageiros_veiculo = linha[119:122]
            chassi_veiculo = linha[122:143].strip()
            nr_motor_veiculo = linha[143:164].strip()

            veiculos_tupla.append(
                (placa_veiculo, especie_veiculo, modelo_veiculo, tipo_veiculo, categoria_veiculo, cor_veiculo,
                 ano_fabricacao_veiculo, ano_modelo_veiculo, num_passageiros_veiculo, renavam_veiculo,
                 chassi_veiculo, nr_motor_veiculo, municipio_veiculo))

            proprietarios_tupla.append((cpf_proprietario, nome_proprietario))

            prop = ProprietarioImporta(cpf_proprietario, nome_proprietario)

            if prop not in proprietarios:
                proprietarios.append(prop)

            veiculos_proprietarios_tupla.append((chassi_veiculo, cpf_proprietario))



        except Exception as e:
            linhas_problematicas.append({'erro': 'unicode', 'ex': '%s ; %s' % (type(e), e), 'linha': linha})
            continue

    cur = connection.cursor()

    insert_veiculo = '''INSERT INTO detransapp_veiculo (placa, especie_id, modelo_id, tipo_veiculo_id, categoria_id,
cor_id, ano_fabricacao, ano_modelo, num_passageiro, renavam, chassi, nr_motor, cidade_id, data, data_alterado)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())'''

    insert_proprietario = '''INSERT INTO detransapp_proprietario (documento,nome) values (%s, %s)'''

    insert_veiculo_proprietario = '''INSERT INTO detransapp_veiculoproprietario (veiculo_id, proprietario_id, data) values (%s, %s, now())'''

    try:
        cur.executemany(insert_veiculo, veiculos_tupla)
        connection.commit()
    except:
        connection.rollback()
        for veiculo in veiculos_tupla:
            try:
                cur.executemany(insert_veiculo, [veiculo])
                connection.commit()
            except Exception as e:
                connection.rollback()
                linhas_problematicas.append(
                    {'erro': 'insert_veiculo', 'ex': '%s ; %s' % (type(e), e), 'linha': veiculo})
                continue

    try:
        cur.executemany(insert_proprietario, proprietarios_tupla)
        connection.commit()
    except:
        connection.rollback()

        for proprietario in proprietarios_tupla:

            try:
                cur.executemany(insert_proprietario, [proprietario])
                connection.commit()
            except psycopg2.IntegrityError:
                connection.rollback()
                continue
            except Exception as e:

                connection.rollback()
                linhas_problematicas.append(
                    {'erro': 'insert_proprietario', 'ex': '%s ; %s' % (type(e), e), 'linha': proprietario})
                continue

    try:
        cur.executemany(insert_veiculo_proprietario, veiculos_proprietarios_tupla)
        connection.commit()
    except:
        connection.rollback()

        for veiculo_proprietario in veiculos_proprietarios_tupla:

            try:
                cur.executemany(insert_veiculo_proprietario, [veiculo_proprietario])
                connection.commit()
            except Exception as e:

                connection.rollback()
                linhas_problematicas.append({'erro': 'insert_veiculo_proprietario', 'ex': '%s ; %s' % (type(e), e),
                                             'linha': veiculo_proprietario})
                continue

    cur.close()

    return linhas_problematicas


class ImportaRenavamThread(threading.Thread):
    def __init__(self, next_n_lines):
        threading.Thread.__init__(self)
        self.next_n_lines = next_n_lines

    def run(self):
        for linha in self.next_n_lines:

            if linha is None or linha.strip() == '':
                continue

            try:
                importa_renavam(linha.strip())
            except:
                continue

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
        for next_n_lines in izip_longest(*[f] * numero_linhas):
            linhas_problematicas.extend(importa_renavam(next_n_lines))

    print 'Fim ', datetime.now()
    print 'Linhas problematicas'
    print linhas_problematicas


def exporta_proprietarios_csv():
    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Inicio ', datetime.now()

    linhas_problematicas = []

    with open('proprietarios.csv', 'w') as csvfile:
        fieldnames = ['documento', 'nome']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for linha in arq.readlines():

            if linha is None or linha.strip() == '':
                continue
            try:
                linha = unicode(linha.strip())

                cpf_proprietario = linha[45:59].strip()
                nome_proprietario = linha[59:119].strip()

                writer.writerow({'documento': cpf_proprietario, 'nome': nome_proprietario})

            except Exception as e:
                linhas_problematicas.append({'erro': 'unicode', 'ex': '%s ; %s' % (type(e), e), 'linha': linha})
                continue

    print 'Fim ', datetime.now()


def remove_linhas_duplicadas_proprietario():
    linhas = open('proprietarios.csv').readlines()
    print 'Count : ', len(linhas)
    uniqlines = set(linhas)
    print 'Count 2 : ', len(uniqlines)
    bar = open('proprietarios2.csv', 'w')

    uniqlines = set(uniqlines)

    bar.writelines(uniqlines)

    bar.close()


def interador(sortedlist):
    a, b = itertools.tee(sortedlist)
    next(b, None)
    r = None
    for k, g in itertools.ifilter(lambda x: x[0][0] == x[1][0], itertools.izip(a, b)):
        if k != r:
            yield k, g
            r = k


def proprietarios_csv_final():
    print 'Inicio : ', str(datetime.now())

    documentos = []

    documentos_gravados = []

    prop3_csv = open('proprietarios3.csv', 'w')
    fieldnames = ['documento', 'nome']

    prop3_writer = csv.DictWriter(prop3_csv, fieldnames=['documento', 'nome'], delimiter=';')
    prop3_writer.writeheader()

    with open('proprietarios2.csv', 'rb') as csvfile:
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


def importa_proprietarios(proprietarios):
    erros_importa_proprietario = []

    cur = connection.cursor()

    insert_proprietario = '''INSERT INTO detransapp_proprietario (documento, nome) values (%s, %s)'''

    count_limit = 10000

    insert_lista = []

    for prop in proprietarios:

        insert_lista.append(prop)

        if len(insert_lista) >= count_limit:

            try:
                cur.executemany(insert_proprietario, insert_lista)
                connection.commit()
            except Exception as e:
                connection.rollback()

                for insert_item in insert_lista:
                    try:
                        cur.executemany(insert_proprietario, [insert_item])
                        connection.commit()
                    except Exception as ex:
                        connection.rollback()

                        erros_importa_proprietario.append(
                            {'erro': 'insert_proprietario', 'ex': '%s ; %s' % (type(ex), ex), 'item': insert_item})
            insert_lista = []
    cur.close()

    return erros_importa_proprietario


'''
Cpf duplicado

[{'nome': 'PEDRO LUIZ MARTINS', 'documento': '00053459059915'}, {'nome': 'ZELIA MARTINS MENDES', 'documento': '00053459059915'}]
'''


def importa_renavam_csv_proprietario():
    print 'Inicio ', datetime.now()

    with open('proprietarios3.csv', 'rb') as csvfile:
        fieldnames = ['documento', 'nome']
        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        proprietarios = []

        for row in dict_render:
            proprietarios.append((row['documento'], row['nome']))

        return importa_proprietarios(proprietarios)

        '''

    numero_linhas = 5000

    linhas_problematicas = []

    with arq as f:

        for next_n_lines in izip_longest(*[f] * numero_linhas):

            importa_proprietarios(next_n_lines)

    print 'Fim ', datetime.now()
    print 'Linhas problematicas'
'''


def teste_documento_duplicado(texto):
    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Inicio ', datetime.now()

    linhas_encontradas = []

    for linha in arq.readlines():
        if texto in linha:
            linhas_encontradas.append(linha)

    print linhas_encontradas


def teste_documento_duplicado_csv(texto):
    arq = open('proprietarios.csv', 'r')
    print 'Inicio ', datetime.now()

    linhas_encontradas = []

    for linha in arq.readlines():
        if texto in linha:
            linhas_encontradas.append(linha)

    print linhas_encontradas


if __name__ == '__main__':
    # print 'Erro etste'
    # extrair_documento_duplicados_error()

    # teste3_utilzando_threads()

    # teste4_sem_thread()


    print 'CSV proprietarios 1'
    exporta_proprietarios_csv()
    print 'CSV proprietarios 2'
    remove_linhas_duplicadas_proprietario()
    print 'CSV proprietarios 3'
    proprietarios_csv_final()
    print 'Inserindo proprietarios'
    importa_renavam_csv_proprietario()

    # print 'Extrair documentos duplicados'
    # extrai_documento_duplicados_proprietario()

    # exporta_proprietarios_doc_validos_csv()

    # print 'CSV importanto proprietarios'
    # erros = importa_renavam_csv_proprietario()



    # count_linhas()
    # leitura_log()

    # Exemplo de documento duplicado, para pessoas diferentes
    # teste_documento_duplicado('00053459059915')
    # teste_documento_duplicado_csv('00053459059915')
