from datetime import datetime
import csv
import operator
import itertools

import teste_importa_renavam_python
import teste_importa_proprietario_python

fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
              'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario']


def busca_registro_duplicados():
    fieldnames = ['chassi', 'renavam', 'placa', 'modelo', 'cor', 'tipo_veiculo', 'especie', 'categoria', 'municipio',
                  'ano_fabricacao', 'ano_modelo', 'nr_passageiros', 'nr_motor', 'proprietario', 'nome_proprietario']
    print 'Inicio : ', str(datetime.now())

    documentos = []

    documentos_gravados = []

    with open('renavam2.csv', 'rb') as csvfile:

        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        # sorted_data = sorted(dict_render, key=operator.itemgetter('chassi'))

        # sortedlist = sorted(dict_render, key=operator.itemgetter('chassi'), reverse=False)

        # list(filter(lambda x: x[0] not in sortedlist, sortedlist))
        # nova_lista = interador(sortedlist)
        # nova_lista = list(nova_lista)

        for group, lines in itertools.groupby(dict_render, key=operator.itemgetter('chassi')):

            if group == '9BD147A0000395307':
                for item in lines:
                    print item

                break
            '''if len(itens) > 1:
                print 'encontro'
                break'''

    print 'Fim : ', str(datetime.now())


def busca_renavam_duplicado():
    print 'Inicio : ', str(datetime.now())

    fieldnames = ['documento', 'nome']

    with open('proprietarios2.csv', 'rb') as csvfile:

        dict_render = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        sortedlist = sorted(dict_render, key=operator.itemgetter('documento'), reverse=False)

        for group, line in itertools.groupby(sortedlist, key=lambda x: x['documento']):
            itens = list(line)
            if len(itens) > 1:
                print 'Encontro'
                break

    print 'Fim : ', str(datetime.now())


if __name__ == '__main__':
    # teste_importa_renavam_python.exporta_renavam_csv()
    # teste_importa_renavam_python.remove_linhas_duplicadas_renavam_csv()
    # busca_registro_duplicados()

    teste_importa_renavam_python.renavam_csv_final()
    teste_importa_proprietario_python.exporta_proprietarios_csv()
    teste_importa_proprietario_python.remove_linhas_duplicadas_proprietario()

    busca_renavam_duplicado()
