import warnings

import router_agent
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import chatbot_agent

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

routerAgent = router_agent.RouterAgent(llm).router_agent
chatbotAgent = chatbot_agent.ChatBotAgent(routerAgent, llm)

if __name__ == "__main__":

    # sql_db.create_database() # Criar o banco a primeira vez que rodar o código, depois comente essa linha para não recriar o banco a cada execução.

    while True:

        pergunta_usuario = input("[Digite sua pergunta ou 'sair' para sair]: ")

        if pergunta_usuario.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o programa.")
            break

        resposta_final = chatbotAgent.chatbot_chain.invoke(pergunta_usuario)

        print('\n' + resposta_final+'\n')

