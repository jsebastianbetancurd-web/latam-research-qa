import os
from loguru import logger
import chromadb
from google import genai
from dotenv import load_dotenv

from populate_db import GeminiEmbeddingFunction

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def format_results(results):
    logger.info(f"Found {len(results['documents'][0])} results.")
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        dist = results['distances'][0][i]
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {meta.get('source')} | Country: {meta.get('country')} | Desk: {meta.get('desk')}")
        print(f"Distance: {dist:.4f}")
        print(f"Content snippet: {doc[:200]}...")

def main():
    client = genai.Client(api_key=GEMINI_API_KEY)
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    collection = chroma_client.get_collection(
        name="citi_internal_research",
        embedding_function=GeminiEmbeddingFunction(client)
    )

    queries = [
        "What is the outlook for Banxico's interest rate given recent inflation?",
        "How is the Mexican peso behaving?",
        "Are there any updates on Chilean lithium strategies?",
        "What are the intervention risks for the Colombian peso?"
    ]
    
    for q in queries:
        print(f"\n\n{'='*50}\nQUERY: {q}\n{'='*50}")
        
        results = collection.query(
            query_texts=[q],
            n_results=3
        )
        format_results(results)

if __name__ == "__main__":
    main()
