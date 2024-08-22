import pandas as pd
import requests
from datetime import datetime

def get_exchange_rate():
    """
    Função para obter a taxa de câmbio do dólar para reais do dia 22/06/2022 usando a API da AwesomeAPI
    """
    url = 'https://economia.awesomeapi.com.br/json/daily/USD-BRL/1?start_date=20220622&end_date=20220622'
    response = requests.get(url)
    data = response.json()
    return float(data[0]['bid'])

def split_fonte_de_recursos(df):
    """
    Função para dividir a coluna 'Fonte de Recursos' em 'ID Fonte Recurso' e 'Nome Fonte Recurso'
    """
    split_cols = df['Fonte de Recursos'].str.split(' - ', expand=True)
    df['ID Fonte Recurso'] = split_cols[0].astype(int)
    df['Nome Fonte Recurso'] = split_cols[1]
    df.drop(columns=['Fonte de Recursos'], inplace=True)
    return df

def clean_numeric_columns(df, column_name):
    """
    Função para limpar e converter colunas numéricas de string para float.
    """
    df[column_name] = df[column_name].str.strip().str.replace('.', '', regex=False).str.replace(',', '.').astype(float).round(2)
    return df

def aggregate_data(df, value_column, new_column_name):
    """
    Função para agregar os dados de despesas ou receitas.
    """
    df_grouped = df.groupby(['ID Fonte Recurso', 'Nome Fonte Recurso']).agg({
        value_column: 'sum'
    }).reset_index()
    df_grouped.rename(columns={value_column: new_column_name}, inplace=True)
    return df_grouped

def merge_dataframes(despesas_df, receitas_df):
    """
    Função para mesclar os DataFrames de despesas e receitas e calcular os totais.
    """
    despesas_df = clean_numeric_columns(despesas_df, 'Liquidado')
    receitas_df = clean_numeric_columns(receitas_df, 'Arrecadado')

    despesas_agg = aggregate_data(despesas_df, 'Liquidado', 'Total Liquidado')
    receitas_agg = aggregate_data(receitas_df, 'Arrecadado', 'Total Arrecadado')

    merged_df = pd.merge(despesas_agg, receitas_agg, on=['ID Fonte Recurso', 'Nome Fonte Recurso'], how='outer').fillna(0)
    
    return merged_df

def add_exchange_rate_columns(df, exchange_rate):
    """
    Função para converter os valores dolarizados para reais e adicionar as colunas convertidas ao DataFrame.
    """
    df['Total Arrecadado'] = (df['Total Arrecadado'] * exchange_rate).round(2)
    df['Total Liquidado'] = (df['Total Liquidado'] * exchange_rate).round(2)
    df['dt_insert'] = datetime.now()
    return df