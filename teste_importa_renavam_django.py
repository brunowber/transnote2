import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.join(BASE_DIR, 'detrans')

import sys

sys.path += [BASE_DIR]

os.environ['DJANGO_SETTINGS_MODULE'] = 'detrans.settings.vilmar'

import chardet
from detransapp.models import Veiculo, Proprietario, Cidade


def count_linhas():
    # arq = codecs.open('detrans_txt/Renavam.txt', encoding='utf-8', mode='r')
    arq = open('detrans_txt/Renavam.txt', 'r')
    arq = arq.readlines()
    print len(arq)


from itertools import izip_longest

import threading

count = 0


def thread_ler(next_n_lines):
    for linha in next_n_lines:
        try:
            unicode(linha)

        except:
            continue


''' 40.239 em 15 minutos o django como responsavel pela insercao no banco'''


def teste2():
    # arq = codecs.open('detrans_txt/Renavam.txt', encoding='utf-8', mode='r')
    arq = open('detrans_txt/Renavam.txt', 'r')

    # arq = codecs.open('detrans_txt/Renavam.txt', 'r', 'UTF-8')

    i = 0
    qtd = 0
    linhas_erro_encoding = []

    for linha in arq:

        if linha.strip() == '':
            continue

        encoding = chardet.detect(linha)

        try:
            linha = linha.encode('utf-8')
        except:
            linhas_erro_encoding.append((linha, encoding['encoding'],))
            continue

        placa = linha[0:7]
        modelo_id = int(linha[7:13])
        cor_id = int(linha[13:15])
        tipo_veiculo_id = int(linha[15:17])
        especie_id = int(linha[17:19])
        categoria_id = int(linha[19:21])
        cidade_id = Cidade.objects.filter(codigo=int(linha[21:26])).values_list('id', flat=True).first()
        renavam = linha[26:37].strip()
        anof = linha[37:41]
        anom = linha[41:45]
        cpf = linha[45:59].strip()
        nome = linha[59:119].strip()
        passageiros = linha[119:122]

        proprietario_id = Proprietario.objects.filter(cpf=cpf).values_list('id', flat=True).first()

        if proprietario_id is None:
            proprietario_id = Proprietario(nome=nome, cpf=cpf)
            proprietario_id.save()
            proprietario_id = proprietario_id.id

        v = Veiculo(placa=placa,
                    modelo_id=modelo_id, cor_id=cor_id, tipo_id=tipo_veiculo_id, especie_id=especie_id,
                    categoria_id=categoria_id,
                    renavam=renavam, ano_fabricacao=anof,
                    ano_modelo=anom, num_passageiro=passageiros,
                    proprietario_id=proprietario_id, cidade_id=cidade_id)
        v.save()

        del proprietario_id

        del v

        qtd += 1
    print(qtd)

    print 'erros linhas: ', linhas_erro_encoding
    print 'erros count : ', len(linhas_erro_encoding)


from datetime import datetime


class ImportaRenavamThread(threading.Thread):
    def __init__(self, next_n_lines):
        threading.Thread.__init__(self)
        self.next_n_lines = next_n_lines

    def run(self):
        for linha in self.next_n_lines:

            if linha is None or linha.strip() == '':
                continue

            try:
                Veiculo.objects.importa_renavam(linha.strip())
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
    387.131 11:55:47  as 12:55 '''


def teste4_sem_thread():
    arq = open('detrans_txt/Renavam.txt', 'r')
    print 'Inicio ', datetime.now()
    for linha in arq.readlines():

        if linha is None or linha.strip() == '':
            continue

        try:
            Veiculo.objects.importa_renavam(linha.strip())
        except:
            continue
    print 'Fim ', datetime.now()


if __name__ == '__main__':
    teste3_utilzando_threads()

    # teste4_sem_thread()
    # count_linhas()
