from prometheus_client import Counter
# Custom Prometheus metrics
api_search_requests_total = Counter("api_search_requests_total", "Total number of /search API calls")
embedding_failures_total = Counter("embedding_failures_total", "Total number of embedding failures")

from fastapi import APIRouter, HTTPException, Query, Body
from app.models import Document
from typing import List, Dict, Any
from app.services.storage import save_document, get_document, delete_document, list_documents
from app.services.rag_pipeline import RAGPipeline
from app.services.rag_pipeline import RAGPipeline


router = APIRouter(prefix="/documents", tags=["documents"])
rag_pipeline = RAGPipeline()


@router.post("/", response_model=Document)
def create_document(doc: Document):
    saved = save_document(doc)
    # Index for retrieval (chunk, embed, store in vector DB)
    rag_pipeline.index_document_for_retrieval(saved)
    return saved

@router.get("/{doc_id}", response_model=Document)
def read_document(doc_id: str):
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/", response_model=list[Document])
def list_docs(title: str | None = Query(default=None, description="Optional title filter"), limit: int = Query(default=50, le=200)):
    return list_documents(title_filter=title, limit=limit)


@router.delete("/{doc_id}")
def remove_document(doc_id: str):
    # Delete raw document
    deleted_doc = delete_document(doc_id)
    # Delete embeddings/chunks
    deleted_embeddings = rag_pipeline.vectordb.delete_embeddings(doc_id)
    if not deleted_doc and deleted_embeddings == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"deleted_document": bool(deleted_doc), "deleted_chunks": deleted_embeddings, "id": doc_id}


# --- /search endpoint ---
@router.post("/search", response_model=List[Dict[str, Any]])
def search_documents(
    query: str = Body(..., embed=True, description="Query string to search for."),
    top_k: int = Body(3, embed=True, description="Number of top results to return."),
):
    """
    Embed the query and return top-k most similar chunks with similarity scores.
    """
    api_search_requests_total.inc()
    try:
        query_embedding = rag_pipeline.embedder.embed_query(query)
    except Exception:
        embedding_failures_total.inc()
        raise
    results = rag_pipeline.vectordb.query_similar(query_embedding, top_k=top_k)
    # Each result: (doc_id, chunk_idx, chunk, distance, metadata)
    # Convert distance to similarity (lower distance = higher similarity)
    return [
        {
            "doc_id": doc_id,
            "chunk_idx": chunk_idx,
            "chunk": chunk,
            "similarity": float(1.0 / (1.0 + distance)),
            "metadata": metadata,
        }
        for doc_id, chunk_idx, chunk, distance, metadata in results
    ]
