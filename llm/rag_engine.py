import os
from google import genai
from google.genai import types

# Define system prompt
SYSTEM_PROMPT = """You are an internal research assistant for Citi Latam Markets.
You answer analyst questions strictly based on the retrieved internal documents provided.

Rules:
1. Always cite your source: document name, date, and page number.
2. If the answer is not in the provided context, say so explicitly — do not infer or hallucinate.
3. If the question involves specific numbers (rates, prices, limits), quote them exactly as written.
4. Be concise. Analysts are time-constrained. Lead with the answer, then the supporting detail.
5. If multiple documents contradict each other, flag the discrepancy and cite both.
"""

# Define query template
QUERY_TEMPLATE = """<context>
{context}
</context>

<question>
{question}
</question>

Answer the question based only on the context above.
Format: 
ANSWER: [direct answer in 1-3 sentences]
SOURCE: [document name · date · page]
DETAIL: [supporting quotes or additional context if needed]
"""

class RAGEngine:
    def __init__(self):
        # Initialize the Gemini GenAI client
        self.client = genai.Client()

    def generate_answer(self, query: str, retrieved_chunks: list[dict]) -> str:
        """
        Synthesize an answer using Gemini based on retrieved chunks.
        """
        # Format the context from retrieved chunks
        context_parts = []
        for chunk in retrieved_chunks:
            meta = chunk.get("metadata", {})
            source_file = meta.get("source_file", "Unknown")
            date = meta.get("date", "Unknown")
            page = meta.get("page", "Unknown")
            text = chunk.get("text", "")
            
            context_parts.append(
                f"[Source: {source_file} | Date: {date} | Page: {page}]\n{text}\n"
            )
            
        context_str = "\n".join(context_parts)
        
        # Build the final prompt
        prompt = QUERY_TEMPLATE.format(context=context_str, question=query)
        
        # Call Gemini 2.5 Flash
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.1, # Low temperature for more factual, document-grounded responses
            )
        )
        
        return response.text
