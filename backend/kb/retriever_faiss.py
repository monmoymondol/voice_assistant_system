# backend/kb/retriever_faiss.py
# Minimal stub: returns empty list if index not built
class DenseRetriever:
    def __init__(self, index_file="kb/kb_faiss_index.pkl"):
        # In a full implementation, load FAISS index and SentenceTransformer
        self.available = False

    def query(self, text, top_k=3):
        # Return empty list until index is built
        return []
