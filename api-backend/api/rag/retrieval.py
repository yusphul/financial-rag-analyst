import os
from typing import Any, Dict, List, Optional
from pinecone import Pinecone
from api.rag.embeddings import embed_texts

def retrieve(query: str, doc_scope: str, top_k: int = 6) -> List[Dict[str, Any]]:
    qvec = embed_texts([query])[0]
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    idx = pc.Index(os.environ["PINECONE_INDEX"])

    pinecone_filter = None
    if doc_scope and doc_scope.upper() != "ALL":
        pinecone_filter = {"doc_scope": {"$eq": doc_scope}}

    res = idx.query(
        vector=qvec,
        top_k=top_k,
        include_metadata=True,
        filter=pinecone_filter,
    )

    hits = []
    for m in (res.get("matches") or []):
        md = m.get("metadata") or {}
        hits.append({
            "id": m.get("id"),
            "score": m.get("score"),
            "doc_id": md.get("doc_id"),
            "source": md.get("source"),
            "location": md.get("location"),
            "text": md.get("text", ""),
        })
    return hits
