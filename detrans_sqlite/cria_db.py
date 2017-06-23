
def criar(conn, cursor):

    cursor.execute("create table if not exists config_sinc ("
                    + "horas_descarte integer, "
                    + "tempo_captura_mov integer,"
                    + "distancia_captura_mov decimal,"
                    + "data_sinc datetime, "
                    + "quantidade_fotos integer)")

    cursor.execute("create table if not exists categoria ("
                    + "codigo integer primary key, "
                    + "descricao text)")

    cursor.execute("create table if not exists agente ("
                    + "id integer primary key, "
                    + "identificacao text, "
                    + "first_name text, "
                    + "last_name text, "
                    + "username text, "
                    + "password text)")

    cursor.execute("create table if not exists bloco ("
                    + "id integer primary key, "
                    + "inicio_intervalo integer, "
                    + "fim_intervalo integer, "
                    + "agente_id integer, "
                    + "ativo boolean, "
                    + "minimo_pag_restantes integer, "
                    + "foreign key(agente_id) references agente(id))")

    cursor.execute("create table if not exists uf ("
                    + "id integer primary key, "
                    + "sigla text, "
                    + "nome text)")

    cursor.execute("create table if not exists cidade ("
                    + "codigo integer primary key, "
                    + "nome text, uf_id integer, "
                    + "foreign key(uf_id) references uf(id))")

    cursor.execute("create table if not exists cor ("
                    + "codigo integer primary key, "
                    + "descricao text)")

    cursor.execute("create table if not exists especie ("
                    + "codigo integer primary key, "
                    + "descricao text)")

    cursor.execute("create table if not exists lei ("
                    + "id integer primary key, "
                    + "lei text)")

    cursor.execute("create table if not exists medida_administrativa("
                    + "id integer primary key, "
                    + "descricao text)")

    cursor.execute("create table if not exists modelo ("
                    + "codigo integer primary key, "
                    + "descricao text)")

    cursor.execute("create table if not exists proprietario("
                    + "id integer primary key autoincrement, "
                    + "nome text, "
                    + "cnh text, "
                    + "documento text)")

    cursor.execute("create table if not exists tipo_infracao ("
                    + "codigo text primary key, "
                    + "descricao text, "
                    + "lei_id integer, "
                    + "is_condutor_obrigatorio boolean,"
                    + "ativo boolean,"
                    + "foreign key(lei_id) references lei(id))")

    cursor.execute("create table if not exists tipo_veiculo ("
                    + "codigo integer primary key, "
                    + "descricao text)")

    cursor.execute("create table if not exists veiculo ("
                    + "chassi VARCHAR(21) primary key, "
                    + "renavam integer, "
                    + "nr_motor text, "
                    + "placa text, "
                    + "modelo_codigo integer, "
                    + "tipo_veiculo_codigo integer, "
                    + "especie_codigo integer, "
                    + "cidade_codigo integer, "
                    + "cor_codigo integer, "
                    + "categoria_codigo integer, "
                    + "ano_fabricacao integer, "
                    + "ano_modelo integer, "
                    + "num_passageiro integer, "
                    + "proprietario_id integer, "
                    + "foreign key(modelo_codigo) references modelo(codigo), "
                    + "foreign key(tipo_veiculo_codigo) references tipo_veiculo(codigo), "
                    + "foreign key(especie_codigo) references especie(codigo), "
                    + "foreign key(cidade_codigo) references cidade(codigo), "
                    + "foreign key(cor_codigo) references cor(codigo), "
                    + "foreign key(categoria_codigo) references categoria(codigo), "
                    + "foreign key(proprietario_id) references proprietario(id))")

    cursor.execute("create table if not exists agente_login ("
                    + "id integer primary key autoincrement, "
                    + "id_agente integer, "
                    + "status integer, "
                    + "imei bigint )")

    cursor.execute("create table if not exists config_det ("
                    + "id integer primary key autoincrement, "
                    + "autuador VARCHAR(15))")
                   

    conn.commit()
