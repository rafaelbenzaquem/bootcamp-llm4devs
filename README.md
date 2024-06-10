# LLM4Devs
Olá, o aplicativo desse repositório foi feito a partir do bootcamp LLM4Devs ministrado pelo professor Gustavo Pinto. O
chatbot foi criado como exercício pós botcamp e tem o objetivo de me auxiliar a estudar para o concurso do Banco 
Central. Os dados coletados para treinamento não serão compartilhados, mas eles incluem o edital atualizado, exemplos 
de provas discursivas do Cebraspe e apostilas das disciplinas, todos em pdfs.
## Ferramentas

Foi utilizado Python como linguagem de programação e uma imagem docker com pgvactor + postgres como banco de dados. 

- Python: 3.10 ou superior
- Docker

Todas as demais dependencias serão instaladas via `pip`.

## Crie um ambiente virtual e instale as dependencias do Python

Para não criar uma confusão com as bibliotecas do seu sistema e as que serão utilizadas , foi criado
um ambiente virtual separado.

No Mac ou Linux
```
python3 -m venv env

source env/bin/activate
```
No windows
```
python -m venv env

./env/bin/activate
```

Em seguida, instale as bibliotecas: 

```
pip install -r requirements.txt
```

## Baixe a imagem do Postgres + Pgvector utilizando Docker com docker-compose

O PGVector é uma ferramenta muito importante para criação de aplicações baseadas em LLMs, uma vez que ele fornece novos 
tipos de armazenamento e busca de dados. Considerando que você já tenha o docker em sua máquina, para utiliza-lo com uma
imagem Postgres, siga as instruções abaixo:

crie um arquivo docker-compose.yaml e copie o código a seguir:

``` yaml

version: '3.9'

services:
  db:
    hostname: db
    image: ankane/pgvector
    ports:
     - 5432:5432
    restart: always
    environment:
      - POSTGRES_DB= ${POSTGRES_DB} # Base de dados será criada ao iniciar o container
      - POSTGRES_USER= ${POSTGRES_USER} # Usuário que será criado ao iniciar o container
      - POSTGRES_PASSWORD= ${POSTGRES_PASSWORD} # Senha do usuário que será criado ao iniciar o container
      - POSTGRES_HOST_AUTH_METHOD=trust
    volumes:
     - ./init.sql:/docker-entrypoint-initdb.d/init.sql # Script sql que será executado ao iniciar o container
     - ./data_sources/postgres-data:/var/lib/postgresql/data # Diretório '/data_sources/postgres-data' no comptuador 
                                                             # hospedeiro armazena os dados do postgres no container
                                                             # '/var/lib/postgresql/data'

```

crie o arquivo 'init.sql' no diretório do docker-compose.yaml e compie o escript a baixo:

```sql 
CREATE EXTENSION IF NOT EXISTS vector;

-- DROP TABLE IF EXISTS embeddings;

CREATE TABLE IF NOT EXISTS edital_bacen (
    id SERIAL PRIMARY KEY,
    content TEXT,
    chars INTEGER,
    embeddings VECTOR
);

CREATE TABLE IF NOT EXISTS nocoes_economia (
    id SERIAL PRIMARY KEY,
    content TEXT,
    chars INTEGER,
    embeddings VECTOR
);

CREATE TABLE IF NOT EXISTS discursiva (
    id SERIAL PRIMARY KEY,
    content TEXT,
    chars INTEGER,
    embeddings VECTOR
);
```

para baixar a imagem, criar, executar o container execute o comando a baixo:

``` bash
docker-compose up
```

## Configure acesso a OpenAI

Muito do nosso trabalho será baseado nas APIs da OpenAI. Para isso, você precisa criar uma chave para acessar a
[plataforma da OpenAI](https://platform.openai.com/). 

Em seguida, adicione a variavel de ambiente `OPENAI_API_KEY` dentro do arquivo `.env`.

```
OPENAI_API_KEY = "<CHAVE>"
```

## Rode a interface web

Por fim, para garantir que a configuracao foi bem sucedida, rode o seguinte comando:

- `python3 $PATH/bootcamp-llm4devs/core/main.py`

## Exercícios pós-bootcamp

Após o bootcamp, para continuar progredindo nos estudos, considere implementar essa lista de exercícios:

- Siga as instruções do BootCamp e implemente uma solução parecida com a que está na branch bootcamp.
- Teste o exercício do bootcamp com outro modelo  (como o Gemini-pro, mistral, etc). 
- Busque novas fontes de dados de outros formatos (arquivos PDFs, vídeos do YouTube).
- Estude como os dados são inseridos no banco. Brinque com os tamanhos e estratégias de chunking.
- Estudo e implemente diferentes estratégias para limpeza de dados. Pense como essas estratégias podem ser utilizadas em
- diferentes tipos de dados (considere tipos de dados como XML, JSON, trechos de código, tabelas, etc). 

Ao longo da sua implementação, usse o Discord para discutir suas soluções.