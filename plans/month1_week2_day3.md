**Month 1 — Week 2 — Day 3 (AI Integration)**

Focus: Embedding and retrieval experiments.

---

### Objective

Integrate an embedding model with your backend and run a retrieval test.

---

### Tasks

1. **Set Up Local Embedding Workflow**

   * Use OpenAI `text-embedding-3-small` for baseline.
   * Alternatively, try a local model (e.g. `sentence-transformers/all-MiniLM-L6-v2`) using `langchain.embeddings.HuggingFaceEmbeddings`.

2. **Chunking Experiment**

   * Split one sample document (e.g. 1–2 pages of financial news) into text chunks using:

     ```python
     from langchain.text_splitter import RecursiveCharacterTextSplitter
     ```

   * Start with chunk size 500, overlap 50.
   * Record retrieval quality as you vary size.

3. **Vector DB Setup**

   * Choose local pgvector (PostgreSQL + pgvector) or Pinecone cloud.
   * Insert and query embeddings using `langchain.vectorstores`.

4. **Simple Retrieval Test**

   * Build a `/search` FastAPI endpoint that:

     * Takes a text query.
     * Embeds it.
     * Returns top-3 matching chunks with similarity scores.

5. **Observation**

   * Measure latency, similarity relevance, and embedding cost (if using API).
   * Record notes for ADR #2 (*RAG design choice*).

---

### Expected Output

* Running `/search` endpoint returning relevant results.
* Notes on local vs cloud embedding trade-offs.
* Early draft of ADR #2 section on embedding model selection.

---

References: weekly cadence day mapping, roadmap milestone alignment, and month 1 plan week 2 AI task definition.
