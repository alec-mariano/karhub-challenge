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

def split_id(df, column_name):
    """
    Função para dividir ID e Coluna
    """
    split_cols = df[column_name].str.split(' - ', expand=True)
    id_column = 'ID ' + column_name
    name_column = 'Nome ' + column_name
    df[id_column] = split_cols[0]
    df[name_column] = split_cols[1]
    df.drop(columns=[column_name], inplace=True)
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
    df_grouped = df.groupby(['ID Fonte de Recursos', 'Nome Fonte de Recursos']).agg({
        value_column: 'sum'
    }).reset_index()
    df_grouped.rename(columns={value_column: new_column_name}, inplace=True)
    return df_grouped

def merge_dataframes(despesas_agg, receitas_agg):
    """
    Função para mesclar os DataFrames de despesas e receitas e calcular os totais.
    """
    merged_df = pd.merge(despesas_agg, receitas_agg, on=['ID Fonte de Recursos', 'Nome Fonte de Recursos'], how='outer').fillna(0)
    
    return merged_df

def apply_exchange_rate(df, column_name):
    """
    Função para converter os valores dolarizados para reais e adicionar as colunas convertidas ao DataFrame.
    """
    exchange_rate = get_exchange_rate()
    df[column_name] = (df[column_name] * exchange_rate).round(2)
    df['dt_insert'] = datetime.now()
    return df