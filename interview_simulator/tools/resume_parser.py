from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO
import os
from typing import Union


# Function to parse the resume
def parse_resume(file_path:str) -> str:
    """
    Extract text from pdf or docx file.
    Returns cleaned text.
    """
    # Get the file extension
    ext = os.path.splitext(file_path)[1]

    # Check if the file is a pdf 
    if ext == '.pdf':
        with open(file_path,"rb") as f:
            reader = PdfReader(f)
            text = []
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text.append(page_text)
            return "\n".join(text).strip()
    
    # Check if the file is a docx
    elif ext in ['.doc','.docx']:
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs).strip()
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .pdf of .doc )")


