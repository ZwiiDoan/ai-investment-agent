For **Month 1, Week 3, Day 3**, per your Month 1 plan and weekly cadence:

### Focus Area — AI Integration

* Task: **Connect retrieval step to LLM prompt**.
* Objective: Complete RAG pipeline linkage — document embeddings → context retrieval → prompt construction → LLM query → API return.

### Expected Output

* Working end-to-end **query flow**: user → API → vector DB → LLM → response.
* Logs showing retrieval and generation steps.
* Updates to **ADR #2 (RAG Design)** documenting:

  * Chosen vector store (e.g., pgvector or Pinecone),
  * Retrieval mechanism (similarity search, top-k, etc.),
  * Prompt structure with contextual injection.

### Optional Enhancements

* Instrument logs with timing or token counts for observability.
* Add Grafana/Prometheus dashboard **only if** you want runtime metrics beyond basic logs (not required this day).

This builds directly on Day 2’s backend query endpoint and completes Week 3’s full RAG integration loop.
