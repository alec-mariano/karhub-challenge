import pandas as pd

def read_csv(file_path, encoding='latin1'):
    """
    Função para ler um arquivo CSV com o encoding especificado.
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding, delimiter=',')
        return df
    except Exception as e:
        raise Exception(f'Erro ao ler o arquivo {file_path}: {e}')