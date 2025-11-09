# Use global meter provider set in main.py
from opentelemetry import metrics

meter = metrics.get_meter(__name__)

api_search_requests_total = meter.create_counter(
    name="api_search_requests_total", description="Total number of /search API calls"
)
embedding_failures_total = meter.create_counter(
    name="embedding_failures_total", description="Total number of embedding failures"
)

from typing import Any


from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel

from app.models import Document
from app.services.rag_pipeline import RAGPipeline
from app.services.storage import delete_document, get_document, list_documents, save_document


class DocumentsRequest(BaseModel):
    docs: list[Document]


class DocumentsResponse(BaseModel):
    docs: list[Document]


router = APIRouter(prefix="/documents", tags=["documents"])
rag_pipeline = RAGPipeline()


@router.post("/", response_model=DocumentsResponse)
def create_documents(request: DocumentsRequest):
    """
    Accepts an object with a 'docs' field (list of documents), saves and indexes each for retrieval.
    Returns an object with the list of saved documents in 'docs'.
    """
    saved_docs = []
    for doc in request.docs:
        saved = save_document(doc)
        rag_pipeline.index_document_for_retrieval(saved)
        saved_docs.append(saved)
    return DocumentsResponse(docs=saved_docs)


@router.get("/{doc_id}", response_model=Document)
def read_document(doc_id: str):
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/", response_model=list[Document])
def list_docs(
    title: str | None = Query(default=None, description="Optional title filter"),
    limit: int = Query(default=50, le=200),
):
    return list_documents(title_filter=title, limit=limit)


@router.delete("/{doc_id}")
def remove_document(doc_id: str):
    # Delete raw document
    deleted_doc = delete_document(doc_id)
    # Delete embeddings/chunks
    deleted_embeddings = rag_pipeline.vectordb.delete_embeddings(doc_id)
    if not deleted_doc and deleted_embeddings == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "deleted_document": bool(deleted_doc),
        "deleted_chunks": deleted_embeddings,
        "id": doc_id,
    }


# --- /search endpoint ---
@router.post("/search", response_model=list[dict[str, Any]])
def search_documents(
    query: str = Body(..., embed=True, description="Query string to search for."),
    top_k: int = Body(3, embed=True, description="Number of top results to return."),
):
    """
    Embed the query and return top-k most similar chunks with similarity scores.
    """
    api_search_requests_total.add(1)
    try:
        query_embedding = rag_pipeline.embedder.embed_query(query)
    except Exception:
        embedding_failures_total.add(1)
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
