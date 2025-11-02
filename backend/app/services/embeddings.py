from typing import List
from sentence_transformers import SentenceTransformer
from tenacity import retry, stop_after_attempt, wait_fixed


class LocalEmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)


    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents (strings) into vectors. Retries on failure."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string into a vector. Retries on failure."""
        embedding = self.model.encode([text], convert_to_numpy=True)[0]
        return embedding.tolist()
