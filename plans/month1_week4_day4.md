**Month 1 — Week 4 — Day 4: Advanced Coding Focus**

### Theme

**Advanced Coding (Testing & Observability)**

### Objectives

* Strengthen code reliability and visibility before wrapping up Month 1 deliverables.
* Prepare for production-grade practices in the upcoming milestone.

### Tasks

1. **Testing**

   * Implement `pytest` unit tests for FastAPI endpoints:

     * Auth (API key/JWT verification).
     * Query and document retrieval.
   * Mock LLM API calls to ensure reproducible results.

2. **Observability**

   * Integrate structured logging (e.g., `structlog` or Python `logging` with JSON formatter).
   * Add timing metrics for each endpoint.
   * Ensure logs include `request_id` and `user_id` fields for traceability.

3. **Metrics Dashboard**

   * Extend existing Prometheus setup to track:

     * Request latency histogram.
     * LLM response time.
     * Document retrieval count.

4. **Code Quality**

   * Run linting (`flake8` or `ruff`) and type checking (`mypy`).
   * Add CI step for automated test and lint run.

### Output

* ✅ Unit-tested FastAPI app with mockable LLM calls.
* ✅ Structured logs and metrics visible in Grafana.
* ✅ Documented improvements for ADR #3 (*Scaling approach: monolith vs microservice*).

Tomorrow (Day 5) will focus on **documentation and ADR refinement** before Month 1 reflection.
