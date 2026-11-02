from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

class ChatBotAgent:
    def __init__(self, router_agent, llm : ChatOpenAI):

        self.router_agent = router_agent
        
        self.llm = llm

        self.chatbot_prompt = PromptTemplate.from_template(
            """Você é um chatbot atendente simpático e extrovertido de uma loja de instrumentos musicais.
            Responda à pergunta de forma educada e amigável com os dados que foram obtidos pelo sistema.
            
            Pergunta: {question}

            Dados obtidos: {obtained_data}
            """
        )

        self.chatbot_chain = ( 
            { "question": RunnablePassthrough(), "obtained_data": self.router_agent } 
            | self.chatbot_prompt 
            | self.llm 
            | StrOutputParser() )