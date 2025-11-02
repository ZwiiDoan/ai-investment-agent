**Month 1 – Week 2 – Day 1: System Design**

**Goal:**
Diagram the detailed data flow for document ingestion → vector database → retrieval.

**Focus:**
Design the RAG (Retrieval-Augmented Generation) ingestion pipeline.

---

### Step 1. Core Flow

1. **Source ingestion**

   * User uploads or fetches document (PDF, HTML, or text).
   * FastAPI service receives file and extracts text.

2. **Chunking & embedding**

   * Split text into semantic chunks (≈500 tokens).
   * Compute embeddings using OpenAI Embeddings API (e.g., `text-embedding-3-small`).

3. **Vector storage**

   * Store each chunk vector in a vector database (e.g., pgvector, Pinecone, or Chroma).
   * Include metadata: document name, section, timestamp.

4. **Retrieval process**

   * When user asks a question, system embeds query and searches for top-k nearest chunks.
   * Retrieved chunks form the **context** for the LLM.

5. **LLM response**

   * FastAPI composes a prompt template with retrieved context.
   * Sends it to the LLM API and returns summarized or analytical output.

---

### Step 2. Components

| Layer      | Component                  | Technology                          |
| ---------- | -------------------------- | ----------------------------------- |
| Ingestion  | API endpoint `/ingest`     | FastAPI, Python                     |
| Processing | Text splitter + embedding  | LangChain / OpenAI API              |
| Storage    | Vector DB                  | PostgreSQL + pgvector (or Pinecone) |
| Retrieval  | API endpoint `/query`      | FastAPI                             |
| AI         | Contextual completion      | OpenAI GPT models                   |
| Monitoring | Logging + retry middleware | Python `logging` + `tenacity`       |

---

### Step 3. Diagram (conceptual)

```
[User Upload/Query]
        ↓
   [FastAPI API]
        ↓
 [Text Splitter + Embedding]
        ↓
 [Vector DB (pgvector)]
        ↓
 [Retriever]
        ↓
 [Prompt Builder + LLM API]
        ↓
 [Response to User]
```

---

### Step 4. Output Artifact

* Create a **diagram** (Mermaid or draw.io) with:

  * Arrows labeled with data type (text, embedding vector, query).
  * Each component block annotated with its main library or tool.

Next day (Week 2 Day 2) extends backend with `/ingest` and `/retrieve` endpoints.
