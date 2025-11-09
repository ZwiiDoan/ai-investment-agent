
# AI Investment Agent Backend

This backend implements a modular, production-grade Retrieval-Augmented Generation (RAG) API for investment research, with robust observability and structured logging.

## API Endpoints

### `/ai/query` (POST)
**Description:** Main RAG endpoint. Accepts a user question, retrieves relevant context, and returns an LLM-generated answer with sources.

**Request:**
```json
{ "question": "What is the current outlook for ASX tech stocks?" }
```

**Response:**
```json
{
	"answer": "...",
	"sources": ["doc1", "doc2"],
	"chunks": ["...", "..."]
}
```

### `/documents/` (POST)
**Description:** Bulk upload and index documents for retrieval.
**Request:** List of document objects.

### `/documents/search` (POST)
**Description:** Embed a query and return top-k most similar document chunks with similarity scores.

### `/documents/{doc_id}` (GET/DELETE)
**Description:** Retrieve or delete a document and its embeddings.

### `/documents/` (GET)
**Description:** List documents, optionally filter by title.

### `/ai/response` (GET)
**Description:** (Dev/test) Echo endpoint for async simulation.

### `/ai/response-sync` (GET)
**Description:** (Dev/test) Echo endpoint for sync simulation.

## Observability & Tracing

### Logging

Structured JSON logs (`logs/app.log`) include `req_id`, `route`, `latency_ms`, `status`, and `trace_id` for trace correlation.

### Metrics (OpenTelemetry → Prometheus)

Exported via `/metrics` and visualized in Grafana:

* `ai_query_time_seconds` (histogram) – end-to-end query latency.
* `ai_retrieval_latency_seconds` (histogram) – vector search time.
* `ai_llm_query_time_seconds` (histogram) – LLM call duration.
* `ai_llm_tokens_total` (counter) – total LLM tokens consumed.
* `api_search_requests_total`, `embedding_failures_total` (counters).

Grafana dashboard: [AI Investment Agent Backend Observability](http://localhost:3001/d/fastapi-observability/ai-investment-agent-backend)

### Tracing (Jaeger)

OpenTelemetry spans are exported to Jaeger at `http://localhost:16686`.

Span structure for `/ai/query`:

```text
ai.query
	├─ embedding.query
	├─ retrieval.vector_search
	└─ llm.call
```

Attributes include: `question.length`, `retrieval.top_k`, `retrieval.result_count`, `sources.count`, `llm.prompt.length`.

Trace/log correlation via `trace_id` in each request log.

### Sampling

Development: 100% sample rate. Production plan: ratio sampler (e.g. 0.2) + always sample errors.

### Retention

Log rotation weekly; metrics retention managed by Prometheus configuration.

## Architecture

* **FastAPI** for API layer
* **PostgreSQL + pgvector** for vector DB
* **OpenAI** for LLM (via async API)
* **Prometheus** and **Grafana** for metrics and dashboards
* **Loguru** for structured logging

## References

* ADR #1 (Language & Framework Choice): See `../adr/adr-1-Language and Framework Choice - Python and FastAPI.md`
* ADR #2 (RAG System Design): See `../adr/adr-2-rag-design-choice.md`

