from typing import Dict, List, Any
import io
import fitz  # pymupdf
import pandas as pd
from docx import Document


def load_document_bytes(filename: str, data: bytes, doc_scope: str) -> List[Dict[str, Any]]:
    lower = filename.lower().strip()
    if lower.endswith(".pdf"):
        return _load_pdf(filename, data, doc_scope)
    if lower.endswith(".docx"):
        return _load_docx(filename, data, doc_scope)
    if lower.endswith(".csv"):
        return _load_csv(filename, data, doc_scope)
    if lower.endswith(".txt"):
        return _load_txt(filename, data, doc_scope)
    raise ValueError(f"Unsupported file type: {filename}")


def _load_pdf(filename: str, data: bytes, doc_scope: str):
    pdf = fitz.open(stream=data, filetype="pdf")
    out = []
    for i in range(len(pdf)):
        text = (pdf[i].get_text("text") or "").strip()
        if text:
            out.append({
                "doc_id": filename,
                "doc_scope": doc_scope,
                "source": filename,
                "location": f"p{i+1}",
                "text": text,
            })
    return out


def _load_docx(filename: str, data: bytes, doc_scope: str):
    d = Document(io.BytesIO(data))
    paras = [(p.text or "").strip() for p in d.paragraphs]
    text = "\n".join([p for p in paras if p]).strip()
    if not text:
        return []
    return [{
        "doc_id": filename,
        "doc_scope": doc_scope,
        "source": filename,
        "location": "docx",
        "text": text,
    }]


def _load_csv(filename: str, data: bytes, doc_scope: str):
    df = pd.read_csv(io.BytesIO(data))
    text = df.to_csv(index=False).strip()
    if not text:
        return []
    return [{
        "doc_id": filename,
        "doc_scope": doc_scope,
        "source": filename,
        "location": "csv",
        "text": text,
    }]


def _load_txt(filename: str, data: bytes, doc_scope: str):
    text = data.decode("utf-8", errors="ignore").strip()
    if not text:
        return []
    return [{
        "doc_id": filename,
        "doc_scope": doc_scope,
        "source": filename,
        "location": "txt",
        "text": text,
    }]
