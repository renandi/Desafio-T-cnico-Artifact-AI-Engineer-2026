import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings

def create_rag_chain():
    # 1. Configura o modelo de embedding MULTILÍNGUE
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    diretorio_chroma = "./chroma_db_pt"

    # 2. Lógica para não reprocessar o PDF à toa
    if not os.path.exists(diretorio_chroma):
        print("Processando PDF e criando banco vetorial pela primeira vez...")
        loader = PyPDFLoader("data/políticas_da_loja.pdf")
        documentos = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(documentos)
        
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=diretorio_chroma
        )
    else:
        print("Carregando banco vetorial existente do disco...")
        vector_store = Chroma(
            persist_directory=diretorio_chroma, 
            embedding_function=embeddings
        )

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # 3. Configuração do LLM
    internal_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.4
    )

    # 4. Cadeia RAG
    template = """Use os trechos de contexto abaixo para responder à pergunta, se possível detalhadamente. 
    Se a resposta não estiver no contexto, diga que não sabe. Não invente informações.

    Contexto:
    {context}

    Pergunta: {question}

    Resposta concisa:"""
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | internal_llm
        | StrOutputParser()
    )

    return rag_chain