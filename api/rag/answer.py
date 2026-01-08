import os
from typing import Any, Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM = """You are a careful financial analyst assistant.
Answer using ONLY the provided sources. If the sources are insufficient, say so.
Always provide citations (source + location).
Never invent figures."""

def generate_answer(question: str, hits: List[Dict[str, Any]]) -> Dict[str, Any]:
    llm = ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        model="gpt-4o-mini",
        temperature=0.1,
    )

    context = "\n\n---\n\n".join(
        [f"[{h['source']} | {h['location']} | score={h['score']}]\n{h['text']}" for h in hits]
    )

    prompt = f"""Question:
{question}

Sources:
{context}

Write:
1) Answer
2) Citations used (bullet list)
"""

    msg = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])

    sources = [{
        "source": h["source"],
        "location": h["location"],
        "score": h["score"],
        "snippet": (h["text"] or "")[:300],
    } for h in hits]

    return {"answer": msg.content, "sources": sources}
