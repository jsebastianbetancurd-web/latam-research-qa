import os
from loguru import logger
import chromadb
from google import genai
from dotenv import load_dotenv

from ingestion.parsers import parse_pdf, extract_metadata_from_filename
from ingestion.chunker import chunk_text

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiEmbeddingFunction:
    """Custom embedding function for ChromaDB to use Gemini embeddings."""
    def __init__(self, client):
        self.client = client
        
    def name(self) -> str:
        return "gemini-embedding-001"
        
    def __call__(self, input: list[str]) -> list[list[float]]:
        embeddings = []
        for text in input:
            try:
                response = self.client.models.embed_content(
                    model="models/gemini-embedding-001",
                    contents=text
                )
                val = response.embeddings[0].values
                embeddings.append(val)
            except Exception as e:
                logger.error(f"Error embedding text: {e}")
                embeddings.append([0.0]*768)
        return embeddings
        
    def embed_query(self, input: list[str]) -> list[list[float]]:
        return self.__call__(input)
        
    def embed_documents(self, input: list[str]) -> list[list[float]]:
        return self.__call__(input)

def main():
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    docs_dir = "test_docs"
    if not os.path.exists(docs_dir):
        logger.error(f"Documents directory {docs_dir} not found. Did you run generate_mocks.py?")
        return
        
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    embedding_func = GeminiEmbeddingFunction(client)
    
    collection_name = "citi_internal_research"
    try:
        chroma_client.delete_collection(collection_name)
    except Exception:
        pass
        
    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=embedding_func
    )
    
    all_chunks = []
    
    for filename in os.listdir(docs_dir):
        if not filename.endswith('.pdf'):
            continue
            
        file_path = os.path.join(docs_dir, filename)
        
        # 1. Parse PDF
        text = parse_pdf(file_path)
        if not text:
            continue
            
        # 2. Extract Metadata
        metadata = extract_metadata_from_filename(filename)
        
        # 3. Chunk
        chunks = chunk_text(text, metadata, chunk_size=300, chunk_overlap=50)
        all_chunks.extend(chunks)
        
    logger.info(f"Adding {len(all_chunks)} chunks to ChromaDB...")
    
    # 4. Ingest into ChromaDB
    if all_chunks:
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]
        documents = [c["text"] for c in all_chunks]
        metadatas = [c["metadata"] for c in all_chunks]
        
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        logger.info("Database population complete!")
    else:
        logger.warning("No chunks to add.")

if __name__ == "__main__":
    main()
