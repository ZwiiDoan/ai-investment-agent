# Month 1 Reflection Journal

Date: 2025-11-16
Period Covered: Month 1 (Weeks 1–4)

## Executive Summary

Month 1 established the foundation: a functional FastAPI + LLM RAG backend, a minimal Next.js UI, core observability (metrics, tracing pathway, structured logging), and architectural clarity through ADRs. The system now has authenticated endpoints, initial performance instrumentation, and a clear monolith-first scaling posture.

---
 
## 1. Hardest Part of the Pipeline to Design

The most challenging component was the **metrics + tracing integration around the RAG pipeline**. Balancing OpenTelemetry’s evolving Python ecosystem (exporter choices, collector configuration) with FastAPI’s async execution—and ensuring Prometheus/Grafana visibility—required iterative refinement. Specific friction points:

- Choosing OTLP export over direct Prometheus scraping (initial confusion around `PrometheusMetricReader` vs collector exposure).
- Designing meaningful application-level metrics (retrieval counts, latency buckets) without prematurely instrumenting every function.
- Ensuring future extensibility: instrumentation needed to be adaptable to later micro-batching, caching layers, and potential service extraction.

This forced careful boundary definition between `services/` (embedding, retrieval, memory) and cross-cutting concerns (telemetry, logging middleware).

## 2. Component to Rewrite Next Month

The **embedding + retrieval orchestration in the RAG pipeline** (currently tightly coupled) would benefit from a refactor toward clearer interface segregation:

- Introduce an internal abstraction (e.g., `EmbeddingProvider` and `RetrievalProvider`) with explicit request/response schemas.
- Prepare a batch-capable embedding path using a micro-batch queue (short window scheduling) to align with Month 2’s performance goals.
- Decouple persistence (vector DB operations) from transformation logic (chunking, embedding) to enable selective scaling or offloading to a dedicated worker/microservice later (Go or Rust implementation).

This rewrite lowers friction for caching insertion (response + vector hit/miss layers) and unlocks cleaner dependency injection for tests.

## 3. Validating System Scalability

A graduated validation approach:

1. **Instrumentation Metrics**: Track p50/p95/p99 latency on embedding + retrieval, cache hit/miss ratios, batch size distributions, and error rates. Use Grafana panels with sparklines + percentile overlays.
2. **Load Testing Baseline**: Use Locust scenarios simulating increasing concurrent user queries (e.g., 10 → 100 → 500 virtual users). Collect throughput (QPS), saturation points, and latency regression curves.
3. **Resource Profiling**: Monitor CPU, memory, and I/O utilization during load; correlate spikes with specific pipeline phases using trace spans (embedding, retrieval, LLM call).
4. **Scalability Thresholds (Extraction Triggers)**: Define quantitative triggers (e.g., sustained >70% CPU for embeddings module; p95 latency > target for 3 consecutive load stages) to justify service decomposition.
5. **Cost-Performance Trade Studies**: Simulate caching enablement vs no-cache runs to quantify API cost savings (mock/counted OpenAI calls) and latency improvement.
6. **Chaos / Fault Injection (Later)**: Introduce controlled delays in the embedding path to validate resilience of batching and queuing.

## 4. AI Capabilities to Explore Next

Planned priorities:

- **Multi-Agent Orchestration**: Integrate frameworks like LangGraph or AutoGen to coordinate retrieval, summarization, anomaly detection, and strategy generation agents.
- **Tool-Augmented Reasoning**: Introduce structured function-calling (balance sheets, ratio extraction) and a financial analytics toolchain (e.g., lightweight Rust or Go service for numeric computations).
- **Adaptive Prompting**: Prompt templates that adapt based on prior user intent, retrieved sector context, and confidence scores (retrieval overlap + embedding similarity distribution).
- **Response Caching & Semantic Deduplication**: Cache LLM answers keyed by normalized intent + retrieved document hash, with semantic similarity threshold to reuse near-duplicate answers.
- **LLM Ensemble / Arbitration**: Prototype blending (e.g., deterministic financial rules engine + probabilistic LLM narrative) for hybrid outputs, tracked by a confidence metadata schema.
- **Retrieval Quality Scoring**: Use weak supervision (keyword overlap, citation frequency) to assign a retrieval relevance score that influences context window selection.

## Wins & Strengths

- Clear ADR trail accelerates onboarding and future architectural shifts.
- Early observability prevents blind scaling and encourages data-driven evolution.
- Modular monolith structure is disciplined enough for phased extraction.
- CI pipeline ensures baseline code quality (linting, typing, tests) without manual intervention.

## Gaps & Risks

- Limited test coverage on failure modes (auth denial, malformed document ingestion).
- No formal cache strategy yet (all prospective designs; risk of over-engineering later without incremental validation).
- Single-point performance hotspots in embedding path could become bottlenecks before refactor lands.
- Lack of end-to-end synthetic tracing that tags user journeys (frontend → backend → LLM).

## Mitigation Roadmap (Early Month 2)

- Add integration tests simulating multi-step queries with mock embeddings.
- Implement minimal in-memory LRU for vector retrieval results to capture baseline hit rates.
- Introduce trace context propagation from frontend (inject request ID header) to correlate UI actions.
- Draft interface schemas for future embedding microservice and document them in a new ADR.

## Personal Reflection

Designing for scalability before real scale is a balancing act—iterative grounding via instrumentation avoided premature complexity. The next stretch is about elevating intelligence (multi-agent coordination) while keeping the foundation lean. Structured decision logging made pivots lower friction; continuing that discipline will compound long-term clarity.

## Action Items Summary

- Refactor embedding/retrieval into clear provider abstractions.
- Implement baseline caching prototype + hit/miss metrics.
- Define extraction triggers & add them to a “Scaling Thresholds” ADR.
- Expand test suite for auth + negative paths.

---
End of Month 1 Journal. This document will seed Month 2 planning and ADR expansions.
