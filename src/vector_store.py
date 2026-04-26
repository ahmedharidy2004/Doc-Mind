from langchain_chroma import Chroma
from embeddings import get_embedding_model
import os

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def create_vector_store(chunks):
    embedding_model = get_embedding_model()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR
    )
    print(f"Vector store created and saved to {CHROMA_DIR}")
    return vectorstore

def load_vector_store():
    embedding_model = get_embedding_model()
    vectorstore = Chroma(
        embedding_function=embedding_model,
        persist_directory=CHROMA_DIR
    )
    print(f"Vector store loaded from {CHROMA_DIR}")
    return vectorstore