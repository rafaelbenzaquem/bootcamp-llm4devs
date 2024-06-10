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