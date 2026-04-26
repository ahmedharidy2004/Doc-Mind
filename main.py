import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

def main():
    # 1. Load your API key from the .env file
    load_dotenv()
    
    # 2. Initialize the LLM (Step 5 in your diagram)
    # Using 'gpt-4o-mini' to save your credits while testing
    llm = ChatOpenAI(model="gpt-4o-mini")

    print("--- LangChain RAG Test ---")
    
    # 3. Simple Test: Asking a question directly
    # In a full RAG, 'context' would come from your Vector Database (Step 3 & 4)
    query = "What are the first three steps of Data Preparation in RAG?"
    
    try:
        print(f"Sending Query: {query}")
        response = llm.invoke(query)
        
        print("\n--- Response ---")
        print(response.content)
        
    except Exception as e:
        print(f"\nSomething went wrong: {e}")
        print("Check if your API key in .env is correct and has 'All' permissions.")

if __name__ == "__main__":
    main()