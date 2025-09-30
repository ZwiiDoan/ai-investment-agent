# Month 1 Plan — AI Investment Agent v1.0 Kickstart

## Objectives

- Stand up a minimal **end-to-end AI pipeline** (FastAPI → LLM → response).
- Capture your first **architecture diagram**.
- Write your **first ADR** (language choice).

---

## Week 1

- **System Design (Day 1):** Sketch high-level architecture of AI Investment Agent: user → frontend → API → vector DB → LLM.
- **Backend (Day 2):** Set up Python + FastAPI project.
- **AI Integration (Day 3):** Call OpenAI API (or Hugging Face) from FastAPI.
- **Advanced Coding (Day 4):** Add async endpoint + logging.
- **Documentation (Day 5):** Draft ADR #1 — *Why Python + FastAPI as the base*.
- **Frontend (Day 6):** Create Next.js “Hello World” page.
- **Reflection (Day 7):** Journal: risks, open questions, next steps.

---

## Week 2

- **System Design:** Diagram detailed data flow for document ingestion → vector DB → retrieval.
- **Backend:** Add endpoint for storing/retrieving documents.
- **AI Integration:** Experiment with embeddings API + pgvector or Pinecone.
- **Advanced Coding:** Add error handling + retries.
- **Documentation:** Refine ADR #1. Start ADR #2 — *RAG design choice*.
- **Frontend:** Display static “sample insights” page.
- **Reflection:** Record what worked, where you struggled.

---

## Week 3

- **System Design:** Diagram end-to-end user flow (UI → API → DB → AI).
- **Backend:** Implement query endpoint (user asks → system fetches context → AI responds).
- **AI Integration:** Connect retrieval step to LLM prompt.
- **Advanced Coding:** Add simple metrics logging.
- **Documentation:** Finalize ADR #2 (RAG).
- **Frontend:** Call query API from Next.js and render response.
- **Reflection:** Capture lessons learned in journal.

---

## Week 4

- **System Design:** Draft first complete system diagram with components labeled.
- **Backend:** Add lightweight auth (API key or JWT).
- **AI Integration:** Fine-tune prompt for financial text summarization.
- **Advanced Coding:** Add unit tests (pytest).
- **Documentation:** Draft ADR #3 — *Scaling approach: monolith vs microservice*.
- **Frontend:** Show results in styled card/table.
- **Reflection:** Summarize Month 1 outputs.

---

## Month 1 Deliverables

1. **Running Demo:**
   - FastAPI backend + LLM integration.
   - Next.js page calling API and showing response.
2. **Architecture Diagram:** high-level + detailed flows.
3. **3 ADRs:**
   - Language choice.
   - RAG design.
   - Scaling strategy.
4. **Architect’s Journal:** 4 weekly reflections.
