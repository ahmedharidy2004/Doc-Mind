from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from vector_store import load_vector_store

prompt_template = """You are a helpful and accurate assistant. Use the provided context to answer the user's question as precisely as possible. If the context does not contain enough information to answer the question, respond with 'I don't know' and do not make up information.

Context: {context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(prompt_template)

def run_pipeline(query, model_name="llama3", k=2):
    llm = OllamaLLM(model=model_name)
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = chain.invoke(query)

    print(f"\nAnswer : {result}")
    return result

    return result

if __name__ == "__main__":
    query = "What departments are available in Cairo University Faculty of Engineering?"
    run_pipeline(query)