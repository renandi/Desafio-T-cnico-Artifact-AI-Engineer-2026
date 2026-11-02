from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import pdf_rag
import sql_rag

class RouterAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

        self.router_prompt = PromptTemplate.from_template(
            """Você é um roteador inteligente para uma loja de instrumentos musicais.
                Analise a pergunta e decida qual sistema deve responder.
                
                Sistemas:
                - "SQL": Para perguntas sobre vendas, clientes, pedidos, catálogo de produtos e promoções.
                - "PDF": Para perguntas sobre regras da loja, políticas de devolução, trocas e garantias.
                
                Pergunta: {question}
                
                Responda APENAS com a palavra SQL ou PDF:"""
            )

        self.cadeia_classificacao = self.router_prompt | self.llm | StrOutputParser()

        # Construção do Agente Roteador
        self.router_agent = (
            {"classificacao": self.cadeia_classificacao, "question": RunnablePassthrough()}
            | RunnableLambda(lambda info: self.delegar_tarefa(info))
        )

    def delegar_tarefa(self, info):
        classificacao = info["classificacao"].strip().upper()
        pergunta = info["question"]
        
        print(f"\n[Router Agent delegou para: {classificacao}]\n")
        
        if "SQL" in classificacao:
            # Chama o agente do banco de dados
            resposta_sql = sql_rag.create_sql_chain().invoke(pergunta)
            return resposta_sql["output"]
        else:
            # Chama a chain do ChromaDB
            return pdf_rag.create_rag_chain().invoke(pergunta)