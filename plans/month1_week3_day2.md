**Month 1 – Week 3 – Day 2: Core Backend Coding (1h)**

**Goal:** Implement the *query endpoint* for the AI Investment Agent.

---

### Tasks

1. **Define API route**

   * Create `/query` POST endpoint in FastAPI.
   * Accept JSON:

     ```json
     { "question": "What is the current outlook for ASX tech stocks?" }
     ```

2. **Integrate retrieval**

   * Connect to your vector DB (pgvector or Pinecone).
   * Retrieve top-k (e.g., 3–5) relevant document chunks using embedding similarity.

3. **Construct LLM prompt**

   * Combine retrieved context + user query:

     ```
     Context:
     {retrieved_texts}

     Question:
     {user_question}

     Answer clearly and concisely.
     ```

4. **Call LLM**

   * Use OpenAI API (or local model) to generate response.
   * Return structured response:

     ```json
     {
       "answer": "...",
       "sources": ["doc1", "doc2"]
     }
     ```

5. **Log metrics**

   * Record query time, tokens used, and retrieval latency.

---

### Output

* Working `/query` endpoint that chains:
  **question → retrieval → LLM → JSON response**
* Example test:

  ```bash
  curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize today’s ASX market news"}'
  ```

---

Tomorrow (Day 3): Connect LLM and vector DB retrieval for real query flow validation.
