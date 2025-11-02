# ADR #2 – RAG Design Choice

> Status: Proposed (Month 1, Week 2)

## Table of Contents
1. Context
2. Decision
3. Architecture Snippet
4. Alternatives Considered
5. Consequences
6. Observability & Metrics
7. Appendix

## 1. Context

To ground LLM answers in factual, up-to-date data, we use Retrieval-Augmented Generation (RAG). This approach enables the system to ingest documents, chunk and embed them, store vectors in a vector DB, and retrieve relevant context for LLM completions. The pipeline ensures answers are based on stored knowledge, not just model pretraining.

**Data Flow:**

```
[User Query] → [FastAPI Backend] → [Vector DB Search] → [Top-k Chunks] → [LLM Completion]
```

- Document → Chunking → Embedding → Vector DB → Retrieval → LLM Prompt

## 2. Decision

Adopt a modular RAG pipeline using embeddings and vector search (pgvector or Pinecone):
- Ingest documents, chunk and embed them (local or OpenAI model).
- Store embeddings in a vector DB (PostgreSQL+pgvector or Pinecone).
- On user query, embed the query and retrieve top-k similar chunks.
- Compose LLM prompt with retrieved context for factual, grounded answers.

## 3. Architecture Snippet

```
[User Query] → [FastAPI Backend] → [Vector DB Search] → [Top-k Chunks] → [LLM Completion]
```

## 4. Alternatives Considered

- **Fine-tuning LLMs:**
  - Pros: Model learns domain-specific knowledge.
  - Cons: Costly, slow iteration, less flexible for new data.
- **Hybrid Search (BM25 + Dense Embeddings):**
  - Pros: Combines lexical and semantic search for better recall.
  - Cons: More complex, requires additional infrastructure.

## 5. Consequences

- **Pros:**
  - Factual accuracy, lower hallucination risk.
  - Modular retraining and data updates.
  - Scalable and extensible architecture.
- **Cons:**
  - Extra latency (embedding, vector search).
  - Vector DB management overhead.
  - Embedding costs (if using API).

## 6. Observability & Metrics

- **Structured Logging:** JSON logs with request ID, endpoint, latency, and status.
- **Retry Logic:** `tenacity` for resilient embedding and DB calls.
- **Prometheus Metrics:**
  - Standard FastAPI metrics at `/metrics` for Prometheus/Grafana.
  - Custom metrics:
    - `api_search_requests_total`: Counts `/search` API calls.
    - `embedding_failures_total`: Counts embedding errors.

## 7. Appendix

- See also: ADR #1 (Language and Framework Choice)
- Next steps: Implement `/ingest` and `/search` endpoints, prototype with sample documents.
- Updated: [Month 1, Week 2, Day 5]
