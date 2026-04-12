from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from vector_store import load_vector_store

prompt_template = """Use the context below to answer the question.
If you don't know, say you don't know.

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

if __name__ == "__main__":
    query = "What departments are available in Cairo University Faculty of Engineering?"
    run_pipeline(query)
