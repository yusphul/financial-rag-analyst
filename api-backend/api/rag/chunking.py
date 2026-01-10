from typing import Dict, List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""],
)

def chunk_documents(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    for d in docs:
        base = {
            "doc_id": d["doc_id"],
            "doc_scope": d["doc_scope"],
            "source": d["source"],
            "location": d["location"],
        }
        parts = _SPLITTER.split_text(d["text"])
        for idx, t in enumerate(parts):
            cid = f'{base["doc_id"]}::{base["location"]}::c{idx}'
            chunks.append({"id": cid, "text": t, "metadata": {**base, "chunk_index": idx}})
    return chunks
