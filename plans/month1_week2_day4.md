**Month 1 – Week 2 – Day 4: Advanced Coding (1h)**

**Focus:** Observability & Resilience Enhancements

**Objective:** Strengthen the backend with structured logging and error-handling patterns.

---

### Tasks

1. **Add Structured Logging**

   * Integrate `loguru` or Python’s built-in `logging` with JSON output.
   * Include request ID, endpoint, latency, and response status.
   * Example middleware:

     ```python
     import time, logging
     from fastapi import Request

     logger = logging.getLogger("uvicorn.access")

     async def log_requests(request: Request, call_next):
         start = time.time()
         response = await call_next(request)
         duration = time.time() - start
         logger.info(f"{request.method} {request.url.path} completed_in={duration:.3f}s status={response.status_code}")
         return response
     ```

2. **Implement Retry Logic**

   * Use `tenacity` for transient API or DB call retries.
   * Example:

     ```python
     from tenacity import retry, stop_after_attempt, wait_fixed

     @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
     async def call_embedding_api(data):
         ...
     ```

3. **Track Metrics**

   * Add a `/metrics` endpoint returning basic system stats (requests, latency).
   * Optional: integrate `prometheus-fastapi-instrumentator`.

4. **Commit and Document**

   * Commit logging and retry updates.
   * Note decisions and patterns for ADR #2 (*RAG Design Choice*).

---

**Expected Output**

* Backend logs are structured and traceable.
* Retry mechanism in place for unstable external calls.
* Basic metrics available.
* Code and ADR updated.

Aligned with the roadmap’s focus on observability and reliability improvements.
