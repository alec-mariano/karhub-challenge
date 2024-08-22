from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd

from scripts.extract import read_csv
from scripts.transform import get_exchange_rate, split_fonte_de_recursos, merge_dataframes, add_exchange_rate_columns
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

    despesas_df = split_fonte_de_recursos(despesas_df)
    receitas_df = split_fonte_de_recursos(receitas_df)
    merged_df = merge_dataframes(despesas_df, receitas_df)
    exchange_rate = get_exchange_rate()
    final_df = add_exchange_rate_columns(merged_df, exchange_rate)

    kwargs['ti'].xcom_push(key='final_df', value=final_df)

def run_load(**kwargs):
    final_df = kwargs['ti'].xcom_pull(key='final_df', task_ids='run_transform')

    credentials_path = 'karhub_gcp.json' # Substituir suas credenciais aqui
    table_id = 'orcamento.sp_2022' # Nome do seu dataset e tabela

    load_to_bigquery(final_df, table_id, credentials_path)


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