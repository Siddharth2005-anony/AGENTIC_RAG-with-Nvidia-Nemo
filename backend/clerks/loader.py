from pathlib import Path
import fitz
from docx import Document


def load_document(path:Path):
    extension = path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(path)

    elif extension == ".docx":
        return load_docx(path)

    elif extension == ".txt":
        return load_txt(path)

    else:
        raise ValueError("Unsupported file type.")
    

def load_pdf(path:Path):
    doc = fitz.open(path)
    pages = []

    for page in doc:
        pages.append(page.get_text())

    doc.close()

    return "\n".join(pages)

def load_docx(path: Path):
    document = Document(path)

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

def load_txt(path: Path):
    with open(path,"r",encoding="utf-8") as f:
        return f.read()
