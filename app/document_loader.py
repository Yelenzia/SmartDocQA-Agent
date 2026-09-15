from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from docx import Document


def _clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def load_pdf(path: str) -> List[Dict]:
    reader = PdfReader(path)
    docs = []
    for page_no, page in enumerate(reader.pages, start=1):
        text = _clean_text(page.extract_text() or "")
        if text:
            docs.append({
                "text": text,
                "source": Path(path).name,
                "location": f"第 {page_no} 页",
            })
    return docs


def load_docx(path: str) -> List[Dict]:
    document = Document(path)
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    text = _clean_text("\n".join(paragraphs))
    if not text:
        return []
    return [{"text": text, "source": Path(path).name, "location": "正文"}]


def load_txt(path: str) -> List[Dict]:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    text = _clean_text(text)
    if not text:
        return []
    return [{"text": text, "source": Path(path).name, "location": "正文"}]


def load_document(path: str) -> List[Dict]:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path)
    if suffix == ".docx":
        return load_docx(path)
    if suffix == ".txt":
        return load_txt(path)
    raise ValueError(f"暂不支持该文件格式：{suffix}")
