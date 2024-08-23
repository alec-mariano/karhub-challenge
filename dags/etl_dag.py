from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd

from scripts.extract import read_csv
from scripts.transform import apply_exchange_rate, split_id, merge_dataframes, aggregate_data, clean_numeric_columns
from scripts.load import load_to_bigquery

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_extract(**kwargs):
    despesas_path = 'data/gdvDespesasExcel.csv'
    receitas_path = 'data/gdvReceitasExcel.csv'
    despesas_df = read_csv(despesas_path)
    receitas_df = read_csv(receitas_path)
    # Enviando DataFrame para o XCom
    kwargs['ti'].xcom_push(key='despesas_df', value=despesas_df)
    kwargs['ti'].xcom_push(key='receitas_df', value=receitas_df)

def run_transform(**kwargs):
    # Recebendo o DataFrames do XCom
    despesas_df = kwargs['ti'].xcom_pull(key='despesas_df', task_ids='run_extract')
    receitas_df = kwargs['ti'].xcom_pull(key='receitas_df', task_ids='run_extract')

    despesas_df = despesas_df.drop(columns=['Unnamed: 3'])
    despesas_df = despesas_df.head(-1)
    receitas_df = receitas_df.head(-1)

    despesas_df = split_id(despesas_df, 'Fonte de Recursos')
    receitas_df = split_id(receitas_df, 'Fonte de Recursos')

    despesas_df = clean_numeric_columns(despesas_df, 'Liquidado')
    receitas_df = clean_numeric_columns(receitas_df, 'Arrecadado')

    # sp_agg_2022

    despesas_agg = aggregate_data(despesas_df, 'Liquidado', 'Total Liquidado')
    receitas_agg = aggregate_data(receitas_df, 'Arrecadado', 'Total Arrecadado')

    merged_df = merge_dataframes(despesas_agg, receitas_agg)
    merged_df = apply_exchange_rate(merged_df, 'Total Liquidado')
    merged_df = apply_exchange_rate(merged_df, 'Total Arrecadado')

    #sp_des_2022

    despesas_df = split_id(despesas_df, 'Despesa')
    despesas_df = despesas_df.drop('Nome Fonte de Recursos', axis='columns')
    despesas_df = apply_exchange_rate(despesas_df, 'Liquidado')

    #sp_rec_2022

    receitas_df = split_id(receitas_df, 'Receita')
    receitas_df = receitas_df.drop('Nome Fonte de Recursos', axis='columns')
    receitas_df = apply_exchange_rate(receitas_df, 'Arrecadado')

    kwargs['ti'].xcom_push(key='merged_df', value=merged_df)
    kwargs['ti'].xcom_push(key='despesas_df', value=despesas_df)
    kwargs['ti'].xcom_push(key='receitas_df', value=receitas_df)

def run_load(**kwargs):
    merged_df = kwargs['ti'].xcom_pull(key='merged_df', task_ids='run_transform')
    despesas_df = kwargs['ti'].xcom_pull(key='despesas_df', task_ids='run_transform')
    receitas_df = kwargs['ti'].xcom_pull(key='receitas_df', task_ids='run_transform')

    credentials_path = 'karhub_gcp.json' # Substituir suas credenciais aqui
    tables = ['orcamento.sp_agg_2022', 'orcamento.sp_des_2022', 'orcamento.sp_rec_2022'] # Nome do seu dataset e tabela
    dataframes = [merged_df, despesas_df, receitas_df]

    for i in range(len(tables)):
        load_to_bigquery(dataframes[i], tables[i], credentials_path)


with DAG(
    'etl_budget_sp',
    default_args=default_args,
    description='Executa processo ETL carregando os arquivos CSV para o BigQuery na GCP',
    schedule_interval=None,  # DAG executada manualmente
    start_date=days_ago(1),
    catchup=False,  # Não realiza catchup de execuções passadas
) as dag:   

    extract = PythonOperator(
        task_id='run_extract',
        python_callable=run_extract,
        provide_context=True,
    )

    transform = PythonOperator(
        task_id='run_transform',
        python_callable=run_transform,
        provide_context=True,
    )

    load = PythonOperator(
        task_id='run_load',
        python_callable=run_load,
        provide_context=True,
    )

    # Definindo a sequência de execução
    extract >> transform >> load