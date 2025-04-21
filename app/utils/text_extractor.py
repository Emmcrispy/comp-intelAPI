import docx
import fitz  # PyMuPDF

def extract_text_from_file(path: str) -> list:
    ext = path.lower().split('.')[-1]
    if ext == 'docx':
        return parse_docx(path)
    elif ext == 'pdf':
        return parse_pdf(path)
    else:
        raise ValueError("Unsupported file type")

def parse_docx(path: str) -> list:
    doc = docx.Document(path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return [{"description": full_text}]

def parse_pdf(path: str) -> list:
    text = ""
    with fitz.open(path) as pdf:
        for page in pdf:
            text += page.get_text()
    return [{"description": text}]
