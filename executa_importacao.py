import teste_importa_renavam_python

'''


CREATE TABLE veiculo_csv
(
  id serial NOT NULL,
  chassi character varying(21) NOT NULL,
  renavam bigint NOT NULL,
  nr_motor character varying(21) NOT NULL,
  placa character varying(7) NOT NULL,
  ano_fabricacao integer NOT NULL,
  ano_modelo integer NOT NULL,
  num_passageiro character varying(3) NOT NULL,
  categoria integer NOT NULL,
  municipio integer NOT NULL,
  cor integer NOT NULL,
  especie integer NOT NULL,
  modelo integer NOT NULL,
  tipo_veiculo integer NOT NULL,
  proprietario character varying(14) NOT NULL,
  nome_proprietario character varying(60) NOT NULL,
  CONSTRAINT veiculo_csv_pkey PRIMARY KEY (id)
)

'''

if __name__ == '__main__':
    '''print 'CSV exporte Renavam'
    teste_importa_renavam_python.exporta_renavam_csv()
    print 'CSV remove linhas duplicadas renavam'
    teste_importa_renavam_python.remove_linhas_duplicadas_renavam_csv()
    print 'CSV remove chassi duplicados renavam'
    teste_importa_renavam_python.renavam_csv_final()

    teste_importa_proprietario_python.executa_importacao_proprietario()
    teste_importa_renavam_python.executa_importacao_veiculo()'''

    teste_importa_renavam_python.renavam_csv_exporta_veiculo_bd()

    teste_importa_renavam_python.count_renavam_txt()
    teste_importa_renavam_python.count_renavam_csv()



    # print 'Leitura do arquivo renavam, teste de codificacao'
    # teste_importa_renavam_python.teste_unicode_linha()

    # print 'CSV Veiculos chassi duplicados'
    # teste_importa_renavam_python.renavam_csv_chassis_duplicados()

    # chassi = '9BD147A0000395307'
    # print 'Renvam CSV Busca por chassi '
    # teste_importa_renavam_python.teste_chassi_duplicado(chassi)
