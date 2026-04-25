# Project — Internal Research Q&A Assistant

## Goal
The goal of this project is to create a high-fidelity intelligence layer over proprietary internal research documents. It targets the "information overload" problem faced by market analysts by providing a tool that can instantly extract relevant data points, sentiment, and macro-themes from vast libraries of research PDFs, ensuring that no critical insight is overlooked during market shifts.

## Results
The project resulted in a robust research assistant characterized by:
- **High Precision Retrieval**: A semantic retrieval engine that identifies the specific sections of research reports most relevant to an analyst's query.
- **Source-Grounded Synthesis**: An LLM layer that synthesizes answers with strict adherence to the source text, providing automated citations and de-duplicating evidence across multiple reports.
- **Scalable Indexing**: A persistent vector database architecture that allows for the continuous addition of new research memos without degrading performance.
- **Enhanced Productivity**: Significant reduction in the time required to compile cross-report summaries for periodic market reviews or client inquiries.

## Stack
- **Backend**: FastAPI for high-performance semantic search endpoints.
- **Frontend**: Streamlit for a clean, professional analyst workspace.
- **Intelligence**: Gemini 2.5 Flash for nuanced document synthesis and ChromaDB for local vector storage.
