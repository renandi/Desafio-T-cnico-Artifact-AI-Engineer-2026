from langchain_openai import ChatOpenAI
import pandas as pd
from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent


def create_database():
    # Criação do Banco de Dados SQLite local
    engine = create_engine("sqlite:///loja_musica.db")

    # Dicionário mapeando o nome do arquivo para o nome da tabela no SQL
    arquivos_csv = {
        "categories": "data/desafio_tecnico_ai_eng - categories.csv",
        "customers": "data/desafio_tecnico_ai_eng - customers.csv",
        "order_items": "data/desafio_tecnico_ai_eng - order_items.csv",
        "orders": "data/desafio_tecnico_ai_eng - orders.csv",
        "products": "data/desafio_tecnico_ai_eng - products.csv",
        "promotions": "data/desafio_tecnico_ai_eng - promotions.csv"
    }

    # Leitura dos CSVs e inserção no banco de dados
    for nome_tabela, caminho_arquivo in arquivos_csv.items():
        df = pd.read_csv(caminho_arquivo)
        # Salva o DataFrame como uma tabela SQL. replace garante que reescreva se rodar de novo.
        df.to_sql(nome_tabela, engine, index=False, if_exists="replace")

    print("Banco de dados loja_musica.db criado com sucesso!")

def create_sql_chain():

    # Conexão do LangChain ao banco de dados
    db = SQLDatabase(engine = create_engine("sqlite:///loja_musica.db"))

    sql_system_rules_prompt = PromptTemplate.from_template("""Você é um assistente de IA especializado em consultas SQL para uma loja de instrumentos musicais.

    Responda sempre em Português Brasileiro.
    
    FILTRAGEM EXATA: Se o usuário pedir um instrumento específico (ex: "violão"), você DEVE usar a cláusula WHERE para filtrar nas colunas name e description do produto. (usando LIKE '%nome%').
    
    Para consultas de produtos, leve em consideração o preço, a categoria na qual o produto está cadastrado, a descrição do produto e a disponibilidade em estoque.
    Se necessário faça junções entre as tabelas para obter informações completas sobre produtos e suas respectivas categorias, pedidos, clientes e promoções.
    Responda a pergunta com detalhes e informações do banco de dados:

    {question}
    """)

    sql_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # Criação do Agente SQL
    sql_agent = create_sql_agent(
        sql_llm,
        db=db,
        agent_type="openai-tools",
        # verbose=True # Mantém o log ativo ver a query SQL gerada no terminal,
    )

    sql_chain = sql_system_rules_prompt | sql_agent

    return sql_chain