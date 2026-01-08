import os
from typing import Dict, List, Any
from pinecone import Pinecone, ServerlessSpec

DIM = 1536  # text-embedding-3-small

def _index():
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    name = os.environ["PINECONE_INDEX"]
    cloud = os.getenv("PINECONE_CLOUD", "aws")
    region = os.getenv("PINECONE_REGION", "us-east-1")

    existing = [i["name"] for i in pc.list_indexes()]
    if name not in existing:
        pc.create_index(
            name=name,
            dimension=DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
        )
    return pc.Index(name)

def upsert_chunks(chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
    idx = _index()
    vectors = []
    for c, v in zip(chunks, embeddings):
        vectors.append({
            "id": c["id"],
            "values": v,
            "metadata": {**c["metadata"], "text": c["text"]},
        })
    for i in range(0, len(vectors), 100):
        idx.upsert(vectors=vectors[i:i+100])
