
-- Function: insert_renavam(character varying, character varying, integer, integer, integer, integer, integer, integer, character varying, character varying, character varying, integer, integer)

-- DROP FUNCTION insert_renavam(character varying, character varying, integer, integer, integer, integer, integer, integer, character varying, character varying, character varying, integer, integer);

CREATE OR REPLACE FUNCTION insert_renavam(
nome_proprietario character varying, 
documento_proprietario character varying, 
modelo_codigo integer, 
cor_codigo integer, 
tipo_veiculo_codigo integer, 
especie_codigo integer, 
categoria_codigo integer, 
municipio_veiculo integer, 
placa_veiculo character varying, 
renavam_veiculo bigint, 
num_passageiros_veiculo integer, 
ano_fabricacao_veiculo integer, 
ano_modelo_veiculo integer,
chassi_veiculo character varying,
nr_motor_veiculo character vary	ing)
  RETURNS void AS
$BODY$
DECLARE
	proprietario_id INTEGER;
	cidade_id INTEGER;
BEGIN

	/*proprietario_id := (select id from detransapp_proprietario where documento = documento_proprietario limit 1);
	
	IF proprietario_id is null THEN
		INSERT INTO detransapp_proprietario(nome, documento) VALUES(nome_proprietario, documento_proprietario) RETURNING id INTO proprietario_id;
	ELSE
		
	END IF;

	cidade_id := (select id from detransapp_cidade where codigo = municipio_veiculo);
	*/
		
	INSERT INTO detransapp_veiculo (
	placa, especie_id, modelo_id, tipo_veiculo_id, categoria_id,
	cor_id, ano_fabricacao, ano_modelo, num_passageiro, renavam, data, 
	data_alterado, chassi, nr_motor) 
	values(
		placa_veiculo, especie_codigo, modelo_codigo, tipo_veiculo_codigo, categoria_codigo,
		cor_codigo, ano_fabricacao_veiculo, ano_modelo_veiculo, num_passageiros_veiculo, 
		renavam_veiculo, now(), now(), chassi_veiculo, nr_motor_veiculo
	);
	
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;