from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)

def embed_msg(message):
    return embeddings.embed_query(message)

def embed_docs(docs):
    return embeddings.embed_documents(docs)