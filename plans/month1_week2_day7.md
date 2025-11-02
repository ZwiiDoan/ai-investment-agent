**Month 1 — Week 2 — Day 7 (Reflection & Planning)**

Tasks for today:

* Review progress from week 2.
* Evaluate what worked and what failed during RAG pipeline setup.
* Identify next week’s priorities and adjust scope for week 3.

---

### Reflection Summary

**Achievements:**

* Designed detailed data flow for document ingestion → vector DB → retrieval.
* Implemented document storage/retrieval API in FastAPI.
* Ran initial embedding experiments (pgvector or Pinecone).
* Drafted ADR #2 outlining RAG design choices.

**Challenges:**

* Embedding quality evaluation remains unclear.
* Integration testing between FastAPI and vector DB requires automation.
* No frontend interaction with backend yet.

**Next Steps (Week 3 Preview):**

* Implement query endpoint that connects vector retrieval to LLM.
* Build basic metrics logging and error tracing.
* Finalize ADR #2.
* Start wiring frontend (Next.js) to call the query API.

**Deliverables Next Week:**

* Working “ask → retrieve → respond” demo.
* ADR #2 complete.
* Updated system diagram including retrieval stage.
