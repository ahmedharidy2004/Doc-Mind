from vector_store import load_vector_store

def retrieve_chunks(query, k=2):
    
    vectorstore = load_vector_store()

    results = vectorstore.similarity_search(query, k=k)

    print(f"\n Top {k} chunks retrieved for query: '{query}'\n")
    for i, doc in enumerate(results):
        print(f"--- Chunk {i+1} ---")
        print(f"Content : {doc.page_content}")
        print(f"Source  : {doc.metadata.get('source', 'unknown')}\n")

    return results

if __name__ == "__main__":
    query = "How do I initialize the system?"
    retrieve_chunks(query)