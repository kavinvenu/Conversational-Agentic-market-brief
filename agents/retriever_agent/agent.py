# retriever_agent.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Retriever Agent")

model = SentenceTransformer('all-MiniLM-L6-v2')

# In-memory FAISS index & documents store (in production, persist/load from disk)
index = None
documents = []

class Document(BaseModel):
    id: str
    text: str

@app.post("/index_documents")
async def index_documents(docs: List[Document]):
    global index, documents
    texts = [doc.text for doc in docs]
    embeddings = model.encode(texts, convert_to_numpy=True)
    d = embeddings.shape[1]

    if index is None:
        index = faiss.IndexFlatL2(d)

    index.add(embeddings)
    documents.extend(docs)
    return {"message": f"Indexed {len(docs)} documents."}

@app.get("/search")
async def search(query: str, top_k: int = 5):
    global index, documents
    if index is None or len(documents) == 0:
        raise HTTPException(status_code=400, detail="No documents indexed yet.")

    query_embedding = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_embedding, top_k)
    results = []
    for idx in I[0]:
        if idx < len(documents):
            results.append({"id": documents[idx].id, "text": documents[idx].text})
    return {"results": results}
