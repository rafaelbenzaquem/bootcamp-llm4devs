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
server_ipv4 = os.getenv("SERVER_IPV4")
server_port = os.getenv("SERVER_PORT")

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

# Criação da interface do chatbot
with gr.Blocks() as chat:
    gr.Markdown("# Concurseiro SuperBot")
    gr.Markdown("Nosso Concurseiro SuperBot está pronto para atender suas perguntas!")
    chatbot = gr.Chatbot(height=400)
    textbox = gr.Textbox(
        placeholder="Estamos com o conteúdo para o concurso do Banco Central do Brasil - BCB em dia, pergunte algo para"
                    " o Concurseiro SuperBot",
        container=False, scale=7)
    examples = gr.Examples(
        examples=["Conceitue microeconomia", "O que você sabe sobre o 'Edital do Bacen 2024'?",
                  "O que é um 'estudo de caso'?"],
        inputs=textbox)
    submit_btn = gr.Button("Enviar", elem_classes=["custom-submit-btn"])
    clear_btn = gr.Button("Limpar")

    def user(message, history):
        return "", history + [[message, None]]

    def bot(history):
        length = len(history)
        message = history[length - 1][0]
        embedded_msg = embed_msg(message)

        table_dictionary = {"edital_bacen": "Assunto sobre o Edital do Banco Central do Brasil - BCB ou Bacen, "
                                            "questionamentos sobre conteúdo programático(o que vai cair na prova),"
                                            " datas de prova, cargos, datas, estrutura da prova e outros assuntos do "
                                            "edital do Bacen",
                            "nocoes_economia": "Conteúdo preparatório da disciplina de conhecimento geral "
                                               "Noções de Economia (Microeconomia e Macroeconomia)",
                            "discursiva": "Conteúdo preparatório para prova discursiva, estruturas e organização da "
                                          "prova discursiva, tipos de textos, texto dissertativo, estudo de casos, "
                                          "padrões de provas discursiva cebraspe, rodadas de temas",
                            "fail": "Este assunto não tem relação ao Edital do Banco Central e nenhuma relação com "
                                    "conteúdo preparatório de 'Noções de Economia' e 'Discursiva P2'"}

        table_name = semantic_decision(embedded_msg, table_dictionary)
        sources_retrieved = None
        comand_system = "Não deixe o usuario fugir da proposta do chat"
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
                 "Você é um bot especialista no edital do concurso do Banco Central do Brasil(BCB ou Bacen) 2024"
                 "deve agir como professor de curso preparatório para alunos que desejam ingressar no Bacen ."),
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
        history[length-1][1] = ""
        for character in response.content:
            history[length-1][1] += character
            time.sleep(0.01)
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