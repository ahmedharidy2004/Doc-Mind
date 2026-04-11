from langchain_community.vectorstores import Chroma
from embeddings import get_embedding_model

def create_vector_store(chunks):
    embedding_model = get_embedding_model()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory='./chroma_db'
    )
    print("Vector store created and saved to ./chroma_db")
    return vectorstore

def load_vector_store():
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        embedding_function=embedding_model,
        persist_directory="./chroma_db"
    )
    print("Vector store loaded from ./chroma_db")
    return vectorstore
