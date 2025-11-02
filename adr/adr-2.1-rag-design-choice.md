# ADR #2: RAG Design Choice

## Observability & Metrics

- **Structured Logging:** All API requests are logged in JSON format with request ID, endpoint, latency, and status for traceability.
- **Retry Logic:** Embedding and vector DB operations use `tenacity` for transient error retries, improving resilience to temporary failures.
- **Prometheus Metrics:**
  - Standard FastAPI metrics are exposed at `/metrics` for Prometheus scraping and Grafana visualization.
  - **Custom metrics implemented:**
    - `api_search_requests_total`: Counts every `/search` API call for usage monitoring.
    - `embedding_failures_total`: Counts embedding errors for reliability tracking.
- **Performance & Cost:**
  - Latency and relevance are acceptable for current use case.
  - Embedding cost is zero for local model; OpenAI API cost is per 1K tokens.
- Further tuning and evaluation will be documented as the system evolves.

These patterns ensure the RAG backend is robust, observable, and production-ready.
  - Cons: Slightly lower quality than latest OpenAI models, requires local resources.
- **Cloud API:** OpenAI `text-embedding-3-small`
  - Pros: State-of-the-art quality, robust scaling, no local resource requirements.
  - Cons: API cost per call, network latency, privacy concerns for sensitive data.

### Chunking Strategy

- **Splitter:** `RecursiveCharacterTextSplitter` (from langchain-text-splitters)
- **Parameters:** Chunk size 500, overlap 50 (tunable)
- **Rationale:** Balances context window size with retrieval granularity. Overlap helps preserve context across chunk boundaries.

### Vector Database

- **Choice:** PostgreSQL with pgvector extension (local, open source)
  - Pros: No vendor lock-in, full control, easy integration with existing stack, supports ANN search.
  - Cons: Slightly more setup/maintenance than managed cloud DBs.
- **Alternative:** Pinecone (cloud vector DB)
  - Pros: Managed, scalable, high performance.
  - Cons: Cost, external dependency, less control.

### Retrieval Pipeline

- Documents are chunked, embedded, and stored in pgvector.
- `/search` endpoint embeds the query and retrieves top-k similar chunks using vector similarity.
- Results include chunk text, similarity score, and metadata.

## Decision

- Use local embedding model (`all-MiniLM-L6-v2`) for baseline, with option to switch to OpenAI API for higher quality if needed.
- Use `RecursiveCharacterTextSplitter` with chunk size 500, overlap 50.
- Use PostgreSQL + pgvector for vector search.
- `/search` endpoint returns top-3 relevant chunks for a query.

## Consequences

- No API cost for embedding, fast local inference.
- Easy to experiment with chunking/embedding parameters.
- Can migrate to cloud embedding/vector DB if scale or quality demands change.
- All design choices are modular and can be swapped with minimal code changes.


## Notes

- Latency and relevance are acceptable for current use case.
- Embedding cost is zero for local model; OpenAI API cost is per 1K tokens.
- Further tuning and evaluation will be documented as the system evolves.

### Observability & Custom Metrics

- **Structured Logging:** All API requests are logged in JSON format with request ID, endpoint, latency, and status for traceability.
- **Retry Logic:** Embedding and vector DB operations use `tenacity` for transient error retries, improving resilience to temporary failures.
- **Prometheus Metrics:**
  - Standard FastAPI metrics are exposed at `/metrics` for Prometheus scraping and Grafana visualization.
  - **Custom metrics implemented:**
    - `api_search_requests_total`: Counts every `/search` API call for usage monitoring.
    - `embedding_failures_total`: Counts embedding errors for reliability tracking.
- These patterns ensure the RAG backend is robust, observable, and production-ready.
