
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


# Executando a aplicação
Para rodar o processo de ETL localmente para o BigQuery, precisaremos clonar o projeto via Git para a máquina local, do arquivo JSON da conta de serviço do seu ambiente BigQuery e instalar o Astro CLI.

### Clonando o repositório
Executar o comando abaixo no terminal e no diretório onde deseja manter o projeto.
```bash
  git clone https://github.com/alec-mariano/karhub-challenge.git
```

### Credenciais do BigQuery
Baixar o arquivo JSON com as credenciais para criar a tabela final no seu ambiente BigQuery. Para minimizar as possibilidades de erros na execução, a conta de serviço deve ter as seguintes permissões:

 - Administrador do BigQuery
 - Administrador do Storage
 - Criador de token de conta de serviço

Caso precise de ajuda com essa etapa, siga o tutorial no link: [Tutorial para baixar as credenciais](https://github.com/alec-mariano/karhub-challenge/blob/main/tutorial_gcp.md)

**IMPORTANTE:** Assim que obtiver o arquivo, o mesmo deve ser colocado no diretório raiz do projeto, renomeado como `karhub_gcp.json`.

### Astro CLI
Caso não tenha o Astro CLI em seu ambiente local, siga os passos abaixo para instalação. Os comandos consideram um ambiente Windows.

**Pré-requisitos:**

 - Docker Desktop
 - Microsoft Hyper-V habilitado.

Com o Windows PowerShell aberto como administrador, execute o comando abaixo:

```bash
  winget install -e --id Astronomer.Astro
```
Se a instalação finalizou com sucesso, você já pode rodar o comando abaixo para confirmar:

```bash
  astro version
```
No diretório raiz do projeto, inicialize o Airflow e seus respectivos contêineres com o comando abaixo:

```bash
  astro dev init
```

Após finalizado o setup do Airflow no projeto, agora você está pronto para iniciar o Airflow com a DAG do projeto já configurada para rodar manualmente e carregar os arquivos fonte de dados para a tabela `orcamento.sp_2022` no seu BigQuery. Utilize o comando abaixo e aguarde a interface web do Airflow abrir:

```bash
  astro dev start
```

Na lista de DAGs deve ser possível ver uma DAG de exemplo e a DAG `etl_budget_sp`, que é o processo que executa o ETL. Execute a DAG em questão para iniciar o ETL. É possível acompanhar o processo de extração, transformação e carga ao entrar no detalhe da DAG.

### Parando o Airflow
Após todos os processos executados com sucesso, está já pode parar os contêineres relacionados ao nosso projeto. Basta executar o comando abaixo:

```bash
  astro dev stop
```

# Análises no BigQuery
Nessa seção do documento, temos as perguntas descritas no desafio. As respostas são respondidas pelas queries que estão no diretório `queries` do projeto. Estão prontas para serem executadas no BigQuery.

1 - Quais são as 5 fontes de recursos que mais arrecadaram?

Reposta na query:
```bash
  queries/question_1.sql
```

2 - Quais são as 5 fontes de recursos que mais gastaram?

Reposta na query:
```bash
  queries/question_2.sql
```

3 - Quais são as 5 fontes de recursos com a melhor margem bruta?

Reposta na query:
```bash
  queries/question_3.sql
```

4 - Quais são as 5 fontes de recursos que menos arrecadaram?

Reposta na query:
```bash
  queries/question_4.sql
```

5 - Quais são as 5 fontes de recursos que menos gastaram?

Reposta na query:
```bash
  queries/question_5.sql
```

6 - Quais são as 5 fontes de recursos com a pior margem bruta?

Reposta na query:
```bash
  queries/question_6.sql
```

7 - Qual a média de arrecadação por fonte de recurso?

Reposta na query:
```bash
  queries/question_7.sql
```

8 - Qual a média de gastos por fonte de recurso?

Reposta na query:
```bash
  queries/question_8.sql
```