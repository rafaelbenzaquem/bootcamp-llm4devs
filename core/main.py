import os
import gradio as gr
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from semantic_decision import semantic_decision
from datetime import datetime
from retriever import retrieve
from embeddings import embed_msg

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
server_ipv4 = os.getenv("SERVER_APP_IPV4")
server_port = os.getenv("SERVER_APP_PORT")

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

# Criação da interface do chatbot
with gr.Blocks() as chat:
    gr.Markdown("#The Professor Chat")
    gr.Markdown("Chat especializado em desenvolvimento de software")
    chatbot = gr.Chatbot(height=400)
    textbox = gr.Textbox(
        placeholder="Pergunte algo para o The Professor Chat.",
        container=False, scale=7)
    examples = gr.Examples(
        examples=["O que é o tdd?", "Qual a diferença entre o tdd top-down do tdd botton-up?",
                  "Quais os passos para implementar o tdd"],
        inputs=textbox)
    submit_btn = gr.Button("Enviar", elem_classes=["custom-submit-btn"])
    clear_btn = gr.Button("Limpar")


    def user(message, history):
        return "", history + [[message, None]]


    def bot(history):
        length = len(history)
        message = history[length - 1][0]
        embedded_msg = embed_msg(message)

        table_dictionary = {"algorithms": "Algoritmos são passos sequenciais para resolver problemas ou realizar "
                                          "tarefas. Eles guiam o comportamento de programas de computador, desde "
                                          "cálculos simples até sistemas complexos de IA. Na prática, são como "
                                          "receitas: instruções claras e detalhadas para alcançar um resultado "
                                          "desejado.",
                            "design_patterns": "Padrões de projeto são soluções comprovadas para problemas recorrentes "
                                               "no design de software. Eles são divididos em três tipos principais: "
                                               "criacionais (como Singleton), estruturais (como Adapter) e "
                                               "comportamentais (como Observer). Essencialmente, são atalhos para "
                                               "criar código mais eficiente e reutilizável. Algum interesse específico "
                                               "em um padrão?",
                            "tdd": "Test-Driven Development (TDD) é uma técnica de desenvolvimento onde você "
                                   "escreve testes antes mesmo do código funcional. O ciclo básico é: escreva"
                                   " um teste que falhe, escreva o código mínimo necessário para passar no "
                                   "teste, e depois refatore o código enquanto mantém todos os testes passando."
                                   " Isso ajuda a garantir que o código seja robusto e fácil de manter.",
                            "fail": "Este assunto não tem relação com 'algorithms','design patterns' e 'tdd'"}

        table_name = semantic_decision(embedded_msg, table_dictionary)
        sources_retrieved = None
        comand_system = "O usuário pode fugir da proposta do chat, responda adequadamente"
        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
        print(f"______________________ INICIO - {data_e_hora_em_texto}")
        print(f"Input User - {message}")
        print(f"Tabela escolhida - {table_name}")
        if table_name != "fail":
            sources_retrieved = retrieve("content", table_name, embedded_msg, 3)
            comand_system = ("Para responder a pergunta do usuário, utilize preferencialmente as seguintes "
                             "referências: {sources_retrieved}")

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "Você é um bot professor de ciência da computação"),
                ("human", "{user_input}"),
                ("system", comand_system),
                ("system", "Considere o histórico de conversa: {history}"),
            ]
        )
        print(f"Output Database - {sources_retrieved}")
        chain = prompt | llm
        response = chain.invoke({"user_input": message, "sources_retrieved": sources_retrieved, "history": history})
        print(f"Output ChatGpt4o - {response}")
        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M:%S')
        print(f"---------------------- FIM - {data_e_hora_em_texto}")
        history[length - 1][1] = ""
        for character in response.content:
            history[length - 1][1] += character
            time.sleep(0.005)
            yield history


    textbox.submit(user, [textbox, chatbot], [textbox, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

    submit_btn.click(user, [textbox, chatbot], [textbox, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: None, None, chatbot, queue=False)

# Lançamento do chat
chat.queue()
chat.launch(share=True, server_name=server_ipv4, server_port=int(server_port))
