import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import CharacterTextSplitter

def load_and_chunk(filename):
    """Load and chunk documents based on file type"""
    file_ext = os.path.splitext(filename)[-1].lower()
    
    if file_ext == ".txt":
        loader = TextLoader(filename, encoding="utf-8")
    elif file_ext == ".pdf":
        loader = PyPDFLoader(filename)
    elif file_ext == ".docx":
        loader = Docx2txtLoader(filename)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = text_splitter.split_documents(documents)
    
    return chunks

if __name__ == "__main__":
    chunks = load_and_chunk("../data/mini_manual.txt")
    print(chunks[0])