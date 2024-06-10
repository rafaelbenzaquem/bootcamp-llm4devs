from pgvector.psycopg2 import register_vector
import psycopg2
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()


def database_params():
    return {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
    }


def test_connection():
    try:
        connection = psycopg2.connect(**database_params())
        cursor = connection.cursor()

        cursor.execute("SELECT 1")

        result = cursor.fetchone()
        print("Conexão com banco bem-sucedida? ", result[0] == 1)
        return result[0]

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar:", error)
    finally:
        # Fechar cursor e conexão
        if connection:
            cursor.close()
            connection.close()


def store(content, embeddings, table_name):
    for i in range(len(content)):
        _store(content[i], embeddings[i], table_name)


def _store(content, embeddings, table_name):
    try:
        conn = psycopg2.connect(**database_params())
        register_vector(conn)
        cur = conn.cursor()

        cur.execute(f"INSERT INTO {table_name} (content, chars, embeddings) VALUES (%s, %s, %s);",
                    (content, len(content), embeddings))

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar:", error)
    finally:
        if conn:
            cur.close()
            conn.commit()
            conn.close()


def retrieve(field, table_name, embeddings, limit):
    try:
        conn = psycopg2.connect(**database_params())
        register_vector(conn)
        cur = conn.cursor()
        embeddings = np.array(embeddings)

        cur.execute(f"""
                    SELECT {field}
                    FROM {table_name} 
                    ORDER BY embeddings <=> %s 
                    LIMIT %s""", (embeddings, limit))

        return cur.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar:", error)
    finally:
        if conn:
            cur.close()
            conn.close()
