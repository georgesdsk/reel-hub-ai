from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingsAdapter:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        try: self.model = SentenceTransformer(model_name)
        except: self.model = None
        self.dimension = 384
    async def generate_embedding(self, text):
        if not self.model or not text: return [0.0] * self.dimension
        embedding = self.model.encode(text[:5000])
        norm = np.linalg.norm(embedding)
        if norm > 0: embedding = embedding / norm
        return embedding.tolist()
