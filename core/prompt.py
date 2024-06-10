import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

    
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

template = ChatPromptTemplate.from_messages(
     [
        ("system", "Você é um bot que deve agir como professor de curso preparatório."),
        ("human", "{user_input}"),
        ("system", "Caso o usuário não determine, responda em no máximo 50 palavras."),
    ]
)

chain = template | llm

messages = chain.invoke({"user_input":"Como será a prova do Cebraspe para analista em tecnologia da informação do Banco Central do Brasil em 2024?"})
print(messages) 