**Month 1, Week 4, Day 3 — AI Integration**

Goal: refine AI integration for your investment agent.

**Tasks**

1. **Prompt Optimization:**

   * Experiment with few-shot examples for financial text summarization.
   * Test structured output (JSON) for consistent downstream parsing.

2. **Retrieval Improvement:**

   * Evaluate retrieval quality from pgvector using similarity thresholds.
   * Log query latency and top-k recall metrics.

3. **Pipeline Validation:**

   * Send full user queries through ingestion → retrieval → LLM → response path.
   * Capture any failure points and latency sources.

4. **Documentation:**

   * Record findings on prompt tuning and retrieval accuracy.
   * Update ADR #3 with scalability implications (e.g., caching, batching).

This aligns with your roadmap’s **AI Investment Agent v1.0** milestone, focused on a complete, working end-to-end pipeline.
