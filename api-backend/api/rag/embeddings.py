import os
from typing import List
from langchain_openai import OpenAIEmbeddings

def embed_texts(texts: List[str]) -> List[List[float]]:
    emb = OpenAIEmbeddings(
        api_key=os.environ["OPENAI_API_KEY"],
        model="text-embedding-3-small",
    )
    return emb.embed_documents(texts)
