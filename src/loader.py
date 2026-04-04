from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def load_and_chunk(filename):
    loader = TextLoader(filename, encoding="utf-8")
    documents = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
    )
    chunks = text_splitter.split_documents(documents)
    
    return chunks

chunks = load_and_chunk("../data/mini_manual.txt")
print(chunks[0])
