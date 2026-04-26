from loader import load_and_chunk
from vector_store import create_vector_store

if __name__ == "__main__":
    chunks = load_and_chunk("../data/mini_manual.txt")
    create_vector_store(chunks)