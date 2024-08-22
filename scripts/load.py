from google.cloud import bigquery
from google.oauth2 import service_account

def create_dataset_if_not_exists(client, project_id, dataset_id):
    """
    Função para criar o dataset no BigQuery se ele não existir.
    """
    dataset_ref = f"{project_id}.{dataset_id}"
    dataset = bigquery.Dataset(dataset_ref)
    try:
        client.get_dataset(dataset)
        print(f"Dataset {dataset_ref} já existe")
    except Exception:
        dataset = client.create_dataset(dataset)
        print(f"Dataset {dataset_ref} criado com sucesso")

def load_to_bigquery(df, table_id, credentials_path):
    """
    Função para carregar o DataFrame para uma tabela existente no BigQuery, e criar o dataset se necessário.
    """
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    
    project_id = credentials.project_id
    dataset_id = table_id.split(".")[0]  # Busca ID do dataset pelo ID da tabela
    create_dataset_if_not_exists(client, project_id, dataset_id)
    
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Bloqueia até que a carga esteja completa
    print(f'{job.output_rows} registros inseridos na tabela {table_id}.')