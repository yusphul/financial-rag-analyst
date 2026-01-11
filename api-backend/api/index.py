import os
from typing import Optional, Any, Dict, List
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

# IMPORTANT: keep your imports consistent with your actual package layout.
# If your folder is: api-backend/api/rag/..., then these should be:
from api.rag.loaders import load_document_bytes
from api.rag.chunking import chunk_documents
from api.rag.embeddings import embed_texts
from api.rag.vectorstore import upsert_chunks
from api.rag.retrieval import retrieve
from api.rag.answer import generate_answer

app = FastAPI()

# Vercel will hit /api/..., so we add a prefix in production
API_PREFIX = os.getenv("API_PREFIX", "")  # set to "/api" on Vercel

class ChatRequest(BaseModel):
    question: str
    doc_scope: Optional[str] = None
    top_k: int = 6

@app.get(f"{API_PREFIX}/health")
def health():
    return {"ok": True}



@app.post("/ingest")
async def ingest(file: UploadFile = File(...), doc_scope: Optional[str] = None):
    scope = doc_scope or "default"

    data = await file.read()
    docs = load_document_bytes(filename=file.filename, data=data, doc_scope=scope)
    chunks = chunk_documents(docs)

    vectors = embed_texts([c["text"] for c in chunks])
    upsert_chunks(chunks=chunks, embeddings=vectors)

    return {"status": "ok", "doc_scope": scope, "chunks": len(chunks), "filename": file.filename}


@app.post("/ingest_many")
async def ingest_many(files: List[UploadFile] = File(...), doc_scope: Optional[str] = None):
    scope = doc_scope or "default"
    results = []

    # process each file independently for clearer feedback
    for f in files:
        try:
            data = await f.read()
            docs = load_document_bytes(filename=f.filename, data=data, doc_scope=scope)
            chunks = chunk_documents(docs)

            vectors = embed_texts([c["text"] for c in chunks])
            upsert_chunks(chunks=chunks, embeddings=vectors)

            results.append({
                "filename": f.filename,
                "status": "ok",
                "chunks": len(chunks),
                "doc_scope": scope
            })
        except Exception as e:
            results.append({
                "filename": f.filename,
                "status": "error",
                "error": str(e),
                "doc_scope": scope
            })

    return {"status": "ok", "doc_scope": scope, "files": results}


@app.post("/chat")
async def chat(req: ChatRequest):
    scope = req.doc_scope or "default"
    hits = retrieve(query=req.question, doc_scope=scope, top_k=req.top_k)
    return generate_answer(question=req.question, hits=hits)
