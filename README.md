# Financial Analyst RAG System (Local → Vercel)

A Retrieval-Augmented Generation (RAG) system that answers questions over **financial documents** (P&L, balance sheets, earnings call transcripts, CSV tables) with **grounded citations**.

You can **upload multiple documents**, group them by **scope** (e.g., `acme_q3_2025`), and ask questions like:
- “What drove gross margin changes YoY? Cite sources.”
- “Compute current ratio and explain the change QoQ (show math).”
- “Summarize guidance from the earnings call and cite the exact lines/pages.”

---

## Features

- ✅ **Multi-document upload** (PDF/DOCX/CSV/TXT)
- ✅ **Scopes** for clean isolation (company/quarter): `doc_scope=acme_q3_2025`
- ✅ **All docs mode**: query across all uploaded scopes
- ✅ **Cited answers**: sources + page/section + snippets
- ✅ **Modern UI**: drag & drop, library panel, chat bubbles, source expanders

---

## Architecture (High-level)

**Frontend (Next.js)**
- Document upload + library
- Chat interface
- Displays citations/snippets

**Backend (FastAPI)**
- `/ingest_many` → parse → chunk → embed → upsert to Pinecone
- `/chat` → retrieve → LLM answer (OpenAI) with citations

**Vector DB**
- Pinecone (serverless)

**LLM**
- OpenAI (embeddings + chat)

---

## Repo Structure

```txt
financial-rag-analyst/
├─ api/                      # FastAPI backend
│  ├─ index.py               # /health, /ingest, /ingest_many, /chat
│  └─ rag/                   # loaders, chunking, embeddings, retrieval, answer
├─ web/                      # Next.js frontend
│  ├─ app/                   # UI + proxy routes
│  └─ package.json
├─ .env                      # local env vars (not committed)
├─ .venv/                    # local python venv (not committed)
└─ README.md


## Prerequisites

- Node.js 18+ (recommended)
- Python 3.11+
- Pinecone account + API key
- OpenAI API key

## Environment Variables

Create a file in repo root named .env:

OPENAI_API_KEY=YOUR_OPENAI_KEY
PINECONE_API_KEY=YOUR_PINECONE_KEY
PINECONE_INDEX=financial-rag-analyst
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1


Note: https://app.pinecone.io/ is the Pinecone dashboard (for keys/index), not an env variable.

## Local Setup (Recommended)
** 1) Backend (FastAPI)

From repo root:

python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install fastapi uvicorn python-multipart pydantic
pip install langchain langchain-openai langchain-text-splitters
pip install pinecone pymupdf python-docx pandas python-dotenv

uvicorn api.index:app --reload --port 8000 --env-file .env


Verify:

http://127.0.0.1:8000/health → {"ok": true}

** 2) Frontend (Next.js)

In a new terminal:

cd web
npm install
npm run dev


Open:

http://localhost:3000

The Next.js app proxies requests to the backend:

/api/ingest_many → http://127.0.0.1:8000/ingest_many

/api/chat → http://127.0.0.1:8000/chat

## How to Use
** Upload
- Enter a scope (e.g., acme_q3_2025)
- Drag & drop one or many documents into the uploader
- Confirm ingestion status in the Document Library

** Ask Questions
- Choose By Scope or All Docs
- Ask your question
- Expand Sources to see page/section citations + snippets

![alt text](image.png)