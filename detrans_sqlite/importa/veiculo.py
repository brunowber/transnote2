# coding: utf-8
from detransapp.models import Veiculo


def importa(self, conn, cursor, stopthread):
    veiculos = Veiculo.objects.get_veiculos_sicronismo(1)
    num_pages = veiculos.paginator.num_pages
    count = 1

    while not stopthread.isSet():
        self.progress =int( float(((count*100) / (num_pages+20))))+20

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

            if stopthread.isSet():
                raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Veiculo"')
        if stopthread.isSet():
            raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Veiculo"')
        cursor.executemany("INSERT INTO veiculo (renavam, chassi, nr_motor, placa, modelo_codigo, tipo_veiculo_codigo, "
                           "especie_codigo, cidade_codigo, cor_codigo, categoria_codigo, ano_fabricacao, ano_modelo,"
                           "num_passageiro, cidade_codigo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tupla_veiculos)
        conn.commit()
        count += 1

        if count > num_pages:
            break

        if not stopthread.isSet():
            veiculos = Veiculo.objects.get_veiculos_sicronismo(count)

    if not stopthread.isSet():
        cursor.execute("CREATE INDEX veiculo_placa_index ON veiculo(placa);")
        conn.commit()

        if stopthread.isSet():
            raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Veiculo"')

    else:
        raise ValueError('Geração detrans.sqlite cancelada, parada ao importar "Veiculo"')
