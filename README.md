
# KarHub - Desafio engenheiro de dados

Olá, avaliador! Essa é a minha solução para o desafio proposto para a vaga de engenheiro de dados. Busquei a simplicidade ao arquitetar e implementar a solução, visto que a quantidade de dados não necessita de uma grande estrutura. Pelo mesmo motivo, optei por não armazenar os dados de origem no Google Cloud Storage. Também não tenho um ambiente propício pra esse tipo de operação, já que o Cloud Storage exige método de pagamento cadastrado para utilização do serviço, ao contrário do BigQuery. Caso não encontre o repositório do desafio, utilize link abaixo para acessar o repositório:

 - [Link do desafio explicado com detalhes](https://github.com/karhub-br/data_engineer_test_v2)

## Stack utilizada

**Python:** Linguagem de programação do projeto na versão 3.12.5 64-bit.

**Docker Desktop:** Como usuário de Windows 10, precisei desse recurso para contenerização.

**Astro CLI:** Ferramenta que agiliza a utilização do Airflow localmente.

**Airflow:** Ferramenta para orquestração da pipeline.

**Google Cloud SDK:** Como a camada de consumo escolhida foi uma tabela no BigQuery, utilizei essa biblioteca pra gerenciar o acesso e a criação do dataset e tabela final.

**SQL:** Linguagem utilizada para realizar as consultas no BigQuery.


## Regras de negócio

#### A tabela final deve conter as colunas ID da fonte de recurso, nome da fonte de recursos, total arrecadado e total liquidado
Chegar nessa estrutura final exigiu uma série transformações. Utilizei desses passos lógicos:

1 - Separar a coluna `Fonte de Recursos` pelo conjunto de caracteres ` - ` gerando as colunas novas `ID Fonte Recurso` e `Nome Fonte Recurso` e excluindo a original do dataframe inicial. Essa operação ocorre na função `split_fonte_de_recursos()`.

2 - Já que as duas fontes de dados contemplavam formas distintas de representar os valores monetários, foi necessário normalizar as respectivas colunas. A função responsável por isso é a `clean_numeric_columns()`.

3 - Implementei a função `aggregate_data()` para agregar os dados de valores contidos na planilha.

4 - Em seguida, utilizei a função `merge_dataframes()` para unificar os dataframes e gerar as colunas `Total Liquidado` e `Total Arrecadado` com os valores convertidos em real de acordo com a taxa de câmbio referente ao dia 22/06/2022, conforme regra de negócio.

Gerando assim o dataframe solicitado inicialmente:


| ID Fonte Recurso   | Nome Fonte Recurso       | Total Liquidado | Total Arrecadado
| :---------- | :--------- | :---------------------------------- | :------|
| 001 | TESOURO-DOT.INICIAL E CRED.SUPLEMENTAR | 9999.99 | 9999.99 |

#### Os valores obitidos acima devem também ser exibidos na cotação do real no dia 22/06/2022 no formato decimal usando a api AwesomeAPI

Resolvido rapidamento na função `get_exchange_rate()` com uma requisição para obter a cotação no endpoint abaixo:
```http
  GET https://economia.awesomeapi.com.br/json/daily/USD-BRL/1?start_date=20220622&end_date=20220622
```

#### Adequar os tipos de dados para os mais apropriados

As colunas numéricas foram ajustadas em suas respectivas funções para os tipos `int` (ID Fonte Recurso) e `float` (Total Liquidado e Total Arrecadado), onde as duas últimas mantiveram duas casas decimais.

#### Para ajudar a identificar registros mais atualizados e para nosso controle de auditoria, precisamos que a tabela final tenha as colunas dt_insert que contenha data/hora de inclusão do registro

Independente de erro de escrita ou não, a regra foi interpretada solicitando acrescentar a coluna `dt_insert` na tabela final. Foi utilizado a função `datetime.now()` para inserir a date e hora em tempo de execução do dataframe antes do início da carga na tabela.

#### Salvar esses dados em uma tabela, preferencialmente no BigQuery

Regra atendida pela função `load_to_bigquery()`. A função também verifica se o dataset existe, criando o dataset e a tabela com os nomes determinados no código, caso não existam.
