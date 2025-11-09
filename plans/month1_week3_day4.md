Advanced Coding and observability. Week 3 Day 4 = add simple metrics logging. Cadence aligns with “Advanced Coding… observability improvements”.

### Objectives

* Emit structured logs for query flow.
* Expose basic Prometheus metrics.
* Minimal Grafana only if useful. Not required today.

### Tasks

1. **Structured logging**

   * Add request ID middleware.
   * Log fields: route, user_id (if any), req_id, latency_ms, status, tokens_in/out, top_k, retrieved_doc_ids.
   * Use JSON format and one line per event.

2. **Metrics**

   * Counters: `api_requests_total{route,status}`, `rag_queries_total{status}`.
   * Histograms: `request_latency_seconds{route}`, `retrieval_latency_seconds`, `llm_latency_seconds`.
   * Gauges: `inflight_requests`, `vector_db_pool_in_use`.
   * Token usage counters: `tokens_prompt_total`, `tokens_completion_total`.

3. **Prometheus exporter**

   * Add `/metrics` endpoint.
   * Scrape config example for local dev.
   * Labels: route, model, vector_backend.

4. **Tracing (optional)**

   * Add OpenTelemetry traces spanning: HTTP → retrieval → LLM call.
   * Propagate `trace_id` into logs.

5. **Error handling**

   * Standardize error responses.
   * Increment `*_error_total` counters on exceptions.

6. **Docs**

   * Update ADR #2 with chosen observability stack and metric names.
   * Note sampling policy and log retention.

### Acceptance

* Hitting query endpoint produces JSON logs with req_id and latencies.
* `/metrics` exposes counters and histograms that increase with traffic.
* A failed LLM call increments error counters.
* Short run test: 20 queries, verify P50/P95 latencies and token totals recorded.

### Stretch (only if time remains)

* Quick Grafana panel for P95 latency and error rate. Keep to two panels.

Source: Month 1 Week 3 Day 4 “Add simple metrics logging”; weekly cadence Day 4 “Advanced Coding… observability improvements”.
