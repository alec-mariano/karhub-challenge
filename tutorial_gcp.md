# Tutorial: Como Criar uma Conta de Serviço na GCP com Papéis Específicos e Baixar o Arquivo JSON

Este tutorial vai te guiar na criação de uma conta de serviço no Google Cloud Platform (GCP) com permissões específicas para BigQuery, Google Cloud Storage e a criação de tokens de serviço. No final, você baixará o arquivo JSON da chave da conta de serviço.

## Passo 1: Acesse o Google Cloud Console

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Se necessário, faça login na sua conta do Google.

## Passo 2: Selecione o Projeto

1. No topo da página, clique no seletor de projetos.
2. Selecione o projeto no qual você deseja criar a conta de serviço. Se você não tem um projeto, crie um novo.

## Passo 3: Navegue até IAM e Admin

1. No menu de navegação à esquerda, clique em **IAM e Admin**.
2. Selecione **Contas de serviço**.

## Passo 4: Crie uma Nova Conta de Serviço

1. Clique em **+ CRIAR CONTA DE SERVIÇO** na parte superior da página.
2. Preencha as informações da conta de serviço:
   - **Nome da conta de serviço**: Dê um nome descritivo para a conta de serviço (ex: `bigquery-storage-admin`).
   - **ID da conta de serviço**: Será preenchido automaticamente com base no nome que você escolher.
   - **Descrição da conta de serviço**: Adicione uma descrição para ajudar a identificar a finalidade desta conta (opcional).
3. Clique em **CRIAR E CONTINUAR**.

## Passo 5: Atribua Papéis (Funções)

1. Na seção **Conceder acesso a este projeto**:
   - No campo **Selecione uma função**, atribua os seguintes papéis:
     - **Administrador do BigQuery**: Pesquise por "Administrador do BigQuery" e selecione.
     - **Administrador do Storage**: Pesquise por "Administrador do Storage" e selecione.
     - **Criador de token de conta de serviço**: Pesquise por "Criador de token de conta de serviço" e selecione.
2. Clique em **CONTINUAR**.

## Passo 6: Configure o Acesso ao Serviço (Opcional)

1. A seção **Conceder aos usuários acesso a esta conta de serviço** permite que você dê acesso a outros usuários para gerenciar esta conta de serviço. Para este tutorial, você pode pular esta etapa clicando em **CONCLUÍDO**.

## Passo 7: Gere a Chave da Conta de Serviço

1. Na página de **Contas de serviço**, encontre a conta de serviço recém-criada.
2. Clique no ícone de três pontos no final da linha dessa conta.
3. Selecione **Gerenciar chaves**.
4. Na aba **Chaves**, clique em **ADICIONAR CHAVE** e selecione **Criar nova chave**.
5. No modal que aparecer, escolha o formato **JSON** e clique em **CRIAR**.
6. O arquivo JSON com a chave da conta de serviço será baixado automaticamente para o seu computador. Guarde este arquivo em um local seguro, pois ele contém as credenciais necessárias para a autenticação da sua aplicação nos serviços do GCP.

## Conclusão

Você criou com sucesso uma conta de serviço no GCP com permissões de administrador no BigQuery, administrador do Storage e criador de token de serviço. O arquivo JSON com as credenciais da conta de serviço foi baixado e está pronto para ser utilizado na sua aplicação. Lembre-se de proteger esse arquivo, pois ele concede acesso aos recursos do seu projeto na GCP.
