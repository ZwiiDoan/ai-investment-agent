**Month 1 – Week 2 – Day 5 (Documentation & ADRs)**

**Focus:** Write or refine Architecture Decision Records (ADRs) — specifically *ADR #2: RAG Design Choice*.
Follows the cadence defined in your weekly planand aligns with Month 1 objectives.

---

### 🎯 Objective

Document your decision-making process for **Retrieval-Augmented Generation (RAG)**:

* Why RAG is used.
* What retrieval and embedding methods are chosen.
* Trade-offs versus alternatives.

---

### ✅ Task Steps

1. **Review system context**
   Reference your document ingestion and embedding pipeline from Week 2 design work.
   Summarize data flow: document → chunking → embedding → vector DB → retrieval → LLM prompt.

2. **Draft ADR #2: RAG Design Choice**

   * **Context:** Describe need for grounding LLM answers on factual, stored data.
   * **Decision:** Choose RAG pipeline using embeddings + vector search (e.g., `pgvector` or `Pinecone`).
   * **Consequences:**

     * Pros: factual accuracy, lower hallucination, modular retraining.
     * Cons: extra latency, vector DB management, embedding costs.

3. **Record Alternatives Considered**

   * Fine-tuning model with custom corpus.
   * Hybrid search (BM25 + dense embeddings).

4. **Add Architecture Snippet**

   ```
   [User Query] → [FastAPI Backend] → [Vector DB Search] → [Top-k Chunks] → [LLM Completion]
   ```

5. **Version and Store**
   Save the file as `adr_002_rag_design.md` in your `/docs/adrs/` directory.

---

### 📦 Output

* Completed **ADR #2 – RAG Design Choice**
* Updated architecture diagram (optional, if changed from prior day)
