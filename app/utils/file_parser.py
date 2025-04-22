import json
from io import StringIO
from pdfminer.high_level import extract_text
from docx import Document

def parse_pdf(file_content: bytes) -> str:
    return extract_text(StringIO(file_content.decode('utf-8')))

def parse_docx(file_content: bytes) -> str:
    document = Document(StringIO(file_content.decode('utf-8')))
    return "\n".join([p.text for p in document.paragraphs])

def parse_json(file_content: bytes) -> str:
    data = json.loads(file_content.decode("utf-8"))
    return data.get("description", "")
