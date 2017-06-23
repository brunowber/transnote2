import ast


def leitura_log():
    arq = open('log.txt', 'r')

    arquivo = arq.readlines()

    print arquivo[0]
    print arquivo[1]

    erros = ast.literal_eval(arquivo[3])
    print "Total de erros : ", len(erros)

    linhas_unicode = []

    linhas_insert = []

    for erro in erros:

        if erro['erro'] == 'unicode':
            linhas_unicode.append({'linha': erro['linha'], 'ex': erro['ex']})

        else:
            linhas_insert.append({'linha': erro['linha'], 'ex': erro['ex']})

    print 'Erros unicode : ', len(linhas_unicode)
    print 'Erros insert : ', len(linhas_insert)

    return linhas_insert



import psycopg2


def teste_insert_veiculo_log():
    conn_string = "host='localhost' dbname='detrans4' user='postgres' password='root'"

    connection = psycopg2.connect(conn_string)
    cur = connection.cursor()

    insert_veiculo = '''INSERT INTO detransapp_veiculo (placa, especie_id, modelo_id, tipo_veiculo_id, categoria_id,
cor_id, ano_fabricacao, ano_modelo, num_passageiro, renavam, data, data_alterado, chassi, nr_motor, cidade_id)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    arq = open('log.txt', 'r')

    arquivo = arq.readlines()

    print arquivo[0]
    print arquivo[1]

    erros = ast.literal_eval(arquivo[3])
    print "Total de erros : ", len(erros)

    linhas_unicode = []

    linhas_insert = []

    for erro in erros:

        if erro['erro'] == 'insert':
            linhas_insert.append({'linha': erro['linha'], 'ex': erro['ex']})

            cur.executemany(insert_veiculo, [erro['linha']])
            connection.commit()
    cur.close()


def get_linhas(linhas_insert):
    arq = open('detrans_txt/Renavam.txt', 'r')

    for linha_insert in linhas_insert[:10]:
        linhas_consulta = []
        error = False

        print 'Linha : ', linha_insert['linha']
        print 'Ex : ', linha_insert['ex']

        '''
        for linha in arq.readlines():


            if linha is None or linha.strip() == '':
                continue


            renavam_arquivo=linha[26:37].strip()
            if int(linha_insert['linha'][9]) == int(renavam_arquivo):
                linhas_consulta.append(linha)

        if error:
            break

        if len(linhas_consulta) >= 2:
            print linhas_consulta
            break'''


if __name__ == '__main__':
    # teste3_utilzando_threads()


    # teste_insert_veiculo_log()
    get_linhas(leitura_log())
    # count_linhas()
    # leitura_log()
