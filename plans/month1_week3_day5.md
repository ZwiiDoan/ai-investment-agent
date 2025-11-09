**Month 1 – Week 3 – Day 5: Documentation & ADRs**

Task focus: finalize **ADR #2 — RAG Design Choice**.

### Objectives

* Review all architectural decisions made for the retrieval-augmented generation (RAG) pipeline.
* Justify your design based on performance, maintainability, and cost.
* Capture trade-offs and possible evolutions for later milestones.

### Steps

1. **Summarize architecture**

   * User → API (FastAPI) → Vector DB (pgvector) → LLM (OpenAI or local model).
   * Context retrieved from embeddings, appended to prompt, then passed to model.

2. **Document rationale**

   * Why RAG instead of fine-tuning.
   * Why pgvector over Pinecone (open-source, local control).
   * How chunking and embedding models were chosen.
   * Retrieval query type (cosine similarity, top-k).

3. **Describe data sources**

   * Local documents, reports, or scraped news.
   * Preprocessing: chunking, embedding, metadata tagging.

4. **Add evaluation metrics**

   * Relevance score, latency, cost per query.

5. **List next steps**

   * Introduce multi-agent orchestration in Month 2.
   * Integrate monitoring for retrieval quality.

Deliverable: 1–2 page ADR file `ADR_002_RAG_Design.md` summarizing the above and stored in `/docs/adr/`.

