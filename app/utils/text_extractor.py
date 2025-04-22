import docx
import fitz  # PyMuPDF
import os

def extract_text_from_file(path: str) -> list[dict]:
    """
    Extract text content from .pdf or .docx files.

    Returns:
        A list of dictionaries with a single key 'description' for each file.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == '.docx':
        return parse_docx(path)
    elif ext == '.pdf':
        return parse_pdf(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def parse_docx(path: str) -> list[dict]:
    doc = docx.Document(path)
    full_text = "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    return [{"description": full_text}]

def parse_pdf(path: str) -> list[dict]:
    text = ""
    with fitz.open(path) as pdf:
        for page in pdf:
            text += page.get_text().strip() + "\n"
    return [{"description": text.strip()}]
