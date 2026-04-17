import os
import pdfplumber
from loguru import logger

def parse_pdf(file_path: str) -> str:
    """Extracts text from a PDF file."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return ""

    logger.info(f"Parsing PDF: {file_path}")
    text_content = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
    except Exception as e:
        logger.error(f"Error parsing PDF {file_path}: {e}")
        return ""
    
    return text_content.strip()

def extract_metadata_from_filename(filename: str) -> dict:
    """Extracts simple metadata based on our mock filename structure.
       e.g. 'Latam_Rates_Strategy_Q1.pdf' -> target_desk, country, etc.
    """
    parts = filename.replace('.pdf', '').split('_')
    country = parts[0] if parts else "Unknown"
    desk = parts[1] if len(parts) > 1 else "Unknown"
    
    return {
        "source": filename,
        "country": country,
        "desk": desk
    }
