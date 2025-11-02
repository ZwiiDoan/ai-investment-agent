**Month 1 — Week 1 — Day 4: Advanced Coding (1h)**

**Objective:** Add async support and logging to the FastAPI backend.
Reference: Week 1 plan specifies “Add async endpoint + logging”; Advanced Coding day is Day 4.

---

### Tasks

1. **Convert endpoint to async**

   * Example:

     ```python
     from fastapi import FastAPI
     import asyncio

     app = FastAPI()

     @app.get("/ai-response")
     async def get_ai_response(prompt: str):
         await asyncio.sleep(0.1)  # simulate I/O
         return {"message": f"Received: {prompt}"}
     ```

2. **Add structured logging**

   * Install and configure `loguru` or `structlog`:

     ```bash
     poetry add loguru
     ```

     ```python
     from loguru import logger

     logger.add("logs/app.log", rotation="1 week")

     @app.middleware("http")
     async def log_requests(request, call_next):
         logger.info(f"Request: {request.method} {request.url}")
         response = await call_next(request)
         logger.info(f"Response status: {response.status_code}")
         return response
     ```

3. **Verify async behavior**

   * Use `ab` or `hey` to load test 100 concurrent requests.
   * Compare performance between sync and async versions.

4. **Commit and document**

   * Update `README.md` with logging and async design notes.
   * Record any findings for inclusion in **ADR #1**.

---

**Deliverable:**
An async-enabled FastAPI endpoint with persistent structured logging.
