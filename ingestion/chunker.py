from loguru import logger
from typing import List, Dict

def chunk_text(text: str, source_metadata: dict, chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict]:
    """
    Splits text into smaller chunks based on character count with overlap.
    """
    if not text:
        return []
        
    logger.info(f"Chunking text from {source_metadata.get('source')} (Length: {len(text)})")
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text_slice = text[start:end]
        
        # Adjust chunk to end on a space to avoid truncating words
        if end < len(text):
            last_space = chunk_text_slice.rfind(' ')
            if last_space != -1:
                end = start + last_space
                chunk_text_slice = text[start:end]
        
        chunk_metadata = source_metadata.copy()
        chunk_metadata["chunk_index"] = len(chunks)
        
        chunks.append({
            "text": chunk_text_slice.strip(),
            "metadata": chunk_metadata
        })
        
        start = end - chunk_overlap
        
    logger.info(f"Created {len(chunks)} chunks.")
    return chunks
