CREATE EXTENSION IF NOT EXISTS vector;

-- DROP TABLE IF EXISTS embeddings;

CREATE TABLE IF NOT EXISTS algorithms (
    id SERIAL PRIMARY KEY,
    content TEXT,
    chars INTEGER,
    embeddings VECTOR
);

CREATE TABLE IF NOT EXISTS design_patterns (
    id SERIAL PRIMARY KEY,
    content TEXT,
    chars INTEGER,
    embeddings VECTOR
);

CREATE TABLE IF NOT EXISTS tdd (
    id SERIAL PRIMARY KEY,
    content TEXT,
    chars INTEGER,
    embeddings VECTOR
);