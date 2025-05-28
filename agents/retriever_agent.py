import faiss
import numpy as np
from utils.embeddings import get_embedding

class RetrieverAgent:
    def __init__(self):
        self.index = None
        self.docs = []
    
    def build_index(self, documents):
        embeddings = [get_embedding(doc) for doc in documents]
        dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype('float32'))
        self.docs = documents

    def retrieve(self, query, top_k=3):
        q_emb = np.array([get_embedding(query)]).astype('float32')
        D, I = self.index.search(q_emb, top_k)
        results = [self.docs[i] for i in I[0]]
        return results
