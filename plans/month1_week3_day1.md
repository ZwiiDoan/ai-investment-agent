**Month 1 — Week 3 — Day 1 plan**

Focus: **System Design**
Topic: **End-to-end user flow**

### Task

Draw a diagram showing the full user flow:
`User (Frontend UI)` → `Next.js Client` → `FastAPI Gateway` → `Vector DB` → `LLM` → `Response`.

### Steps

1. Identify main components:

   * **Frontend:** User input form (investment question).
   * **API Layer (FastAPI):** Handles query requests.
   * **Retrieval Layer:** Fetches related documents from vector DB (e.g., pgvector or Pinecone).
   * **AI Layer:** Sends query and retrieved context to LLM (OpenAI or local model).
   * **Response Pipeline:** Returns AI-generated insight to frontend.

2. Add key interactions:

   * API logs request and timing metrics.
   * Retrieval step runs vector similarity search.
   * LLM prompt structured as *{context + user query}*.
   * Response includes text + confidence score (optional).

3. Deliverable:

   * One **architecture diagram** (end-to-end user flow) with clear arrows and data annotations.
   * Update **ADR #2 (RAG Design)** with this flow description.

Next: Backend implementation (Week 3, Day 2) — query endpoint connecting retrieval and AI layers.
