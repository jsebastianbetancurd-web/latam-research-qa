import os
import sys

# Add parent directory to path to allow importing from root project structure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import chromadb
from google import genai
from loguru import logger
from dotenv import load_dotenv

from llm.rag_engine import RAGEngine
from populate_db import GeminiEmbeddingFunction

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(
    title="Citi Internal Research RAG API",
    description="FastAPI endpoints for querying the Latam Markets semantic search system.",
    version="1.0.0"
)

# Initialize global dependencies
client = None
chroma_client = None
collection = None
rag_engine = None

@app.on_event("startup")
def startup_event():
    global client, chroma_client, collection, rag_engine
    
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in environment.")
        return
        
    # Initialize Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Initialize ChromaDB
    chroma_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db")
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    
    embedding_func = GeminiEmbeddingFunction(client)
    
    try:
        collection = chroma_client.get_collection(
            name="citi_internal_research",
            embedding_function=embedding_func
        )
        logger.info(f"Connected to ChromaDB collection 'citi_internal_research' with {collection.count()} documents.")
    except ValueError:
        logger.error("Collection 'citi_internal_research' not found. Run populate_db.py first.")
        
    # Initialize RAG Engine
    rag_engine = RAGEngine()

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    # Additional filters could go here (e.g., date_range, desk)

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    if not collection:
        raise HTTPException(status_code=500, detail="Database not initialized.")
        
    logger.info(f"Received query: {request.query}")
    
    try:
        # Retrieve relevant documents
        results = collection.query(
            query_texts=[request.query],
            n_results=request.top_k
        )
        
        # Package retrieved chunks
        retrieved_chunks = []
        if results['documents'] and results['documents'][0]:
            docs = results['documents'][0]
            metas = results['metadatas'][0]
            
            for doc, meta in zip(docs, metas):
                retrieved_chunks.append({
                    "text": doc,
                    "metadata": meta
                })
                
        if not retrieved_chunks:
            return QueryResponse(answer="No relevant documents found in the database.", sources=[])
        
        # Synthesize answer using RAG engine
        synthesis = rag_engine.generate_answer(query=request.query, retrieved_chunks=retrieved_chunks)
        
        sources = [chunk["metadata"] for chunk in retrieved_chunks]
        
        return QueryResponse(answer=synthesis, sources=sources)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "collection_count": collection.count() if collection else 0}
