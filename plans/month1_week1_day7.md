**Month 1 – Week 1 – Day 7: Reflection & Planning**

### 1. Progress Review

* **Completed tasks:**

  * ✅ Sketched AI Investment Agent high-level architecture.
  * ✅ Set up Python + FastAPI backend.
  * ✅ Integrated first LLM call.
  * ✅ Added async logging.
  * ✅ Drafted ADR #1 (*Why Python + FastAPI as base stack*).
  * ✅ Built a minimal Next.js frontend.
* **Outcome:** You now have a functional FastAPI service responding to LLM queries and a basic frontend showing output.

### 2. Lessons Learned

* **FastAPI** setup and async model simplify experimentation.
* **OpenAI API integration** requires structured prompts and clear error handling.
* **Next.js** connection clarified the end-to-end flow.
* **Documentation cadence** (ADR + diagram + reflection) helps maintain architectural clarity.

### 3. Risks & Open Questions

* Need to choose **vector DB** next (pgvector vs Pinecone).
* Evaluate **hosting strategy** (local vs managed).
* Clarify **data flow** for document ingestion.
* Confirm **security plan** for API key management.

### 4. Next Week Preview (Week 2)

* Focus: **Document ingestion → Vector storage → Retrieval pipeline.**
* New ADR: *RAG design choice.*
* Add one backend endpoint for storing/retrieving documents.
* Refine ADR #1 and produce your first **data flow diagram**.

### 5. Journal Prompt

Write 5–6 sentences on:

* What went smoothly in setup.
* What bottlenecks occurred.
* What technical decisions you’re least confident in.
* What measurable outcome you’ll aim for next week (e.g., “LLM retrieves context from vector DB in <1s”).

Citations: derived from the week 1 plan and cadence schedule.
