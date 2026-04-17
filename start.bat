@echo off
echo Starting Citi Internal Research Q&A RAG System...
echo.

:: Start FastAPI Backend Background Process
echo [1/2] Starting FastAPI Backend on port 8000...
start /B python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000

:: Wait a few seconds for backend to initialize
timeout /t 5 /nobreak > NUL

:: Start Streamlit UI
echo [2/2] Starting Streamlit UI...
python -m streamlit run frontend/app.py

echo.
echo Application Closed.
