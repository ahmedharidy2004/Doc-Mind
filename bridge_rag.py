from loader import load_and_chunk
from vector_store import create_vector_store
from rag_pipeline import run_pipeline

def main():
    chunks = load_and_chunk("../data/mini_manual.txt")
    create_vector_store(chunks)

    query = "What departments are available in Cairo University Faculty of Engineering?"
    run_pipeline(query, model_name="llama3", k=5)

if __name__ == "__main__":
    main()
