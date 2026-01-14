from sentence_transformers import SentenceTransformer
import faiss

class RAGAgent:
    def __init__(self, llm, documents):
        self.llm = llm
        self.docs = documents
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.index.add(self.embedder.encode(documents))

    def run(self, payload):
        query = payload["query"]
        q_emb = self.embedder.encode([query])
        _, idx = self.index.search(q_emb, 3)

        context = "\n".join(self.docs[i] for i in idx[0])

        prompt = f"""
Answer using ONLY the context.

Context:
{context}

Question:
{query}
"""
        return {
            "type": "rag_answer",
            "content": self.llm.generate(prompt)
        }
