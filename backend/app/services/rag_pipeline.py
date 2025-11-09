from app.models import Document
from app.services.chunking import ChunkingService
from app.services.embeddings import LocalEmbeddingService
from app.services.vectordb import VectorDBService


class RAGPipeline:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.chunker = ChunkingService(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedder = LocalEmbeddingService(model_name=embedding_model)
        self.vectordb = VectorDBService()

    def index_document_for_retrieval(self, doc: Document) -> dict:
        # 1. Chunk the document
        chunks = self.chunker.chunk_text(doc.text)
        # 2. Embed the chunks
        embeddings = self.embedder.embed_documents(chunks)
        # 3. Store in vector DB
        metadata = [{"title": doc.title, **(doc.metadata or {})} for _ in chunks]
        self.vectordb.insert_embeddings(doc.id or doc.title, chunks, embeddings, metadata)
        return {"chunks_indexed": len(chunks)}
