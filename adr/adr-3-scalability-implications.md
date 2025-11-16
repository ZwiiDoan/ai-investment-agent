# ADR #3 – Scaling Approach & Scalability Implications: Monolith First, Caching, Batching, and System Growth

> Status: Accepted (Month 1, Week 4 Day 5)

## Table of Contents

1. Context
2. Decision
3. Scalability Strategies
4. Alternatives Considered
5. Consequences
6. Observability & Metrics
7. Next Steps

## 1. Context

As the AI Investment Agent system matures, supporting more users and larger document sets, scalability becomes a critical concern. The current RAG pipeline (see ADR #2) is designed for modularity and factual accuracy, but must also address performance bottlenecks and cost as usage grows. This ADR documents the key scalability strategies under consideration, including caching, batching, and related architectural patterns.

## 2. Decision

Adopt a layered approach to scalability while starting with a **modular monolith** architecture for the MVP:

- **Architecture Choice (Monolith First)**: Keep all core RAG pipeline components (ingestion, chunking, embeddings, vector retrieval, LLM orchestration) in a single deployable FastAPI service with clear internal module boundaries. Defer microservice decomposition until scale or team size makes isolation beneficial.
- **Caching**: Introduce caching at the vector retrieval and LLM response levels to reduce redundant computation and latency.
- **Batching**: Implement request batching for embedding and LLM calls to improve throughput and resource utilization.
- **Connection Pooling**: Use connection pools for the vector DB and LLM API to handle concurrent requests efficiently.
- **Async Processing**: Leverage FastAPI's async capabilities and background tasks for non-blocking operations.

### 2.1 Architecture Approach: Monolith vs Microservices

| Aspect | Monolith (Chosen) | Microservices (Deferred) |
|--------|-------------------|---------------------------|
| Deployment Complexity | Simple (single artifact) | Higher (orchestrator, networking) |
| Development Velocity | High early-phase | Slower initially due to service boundaries |
| Operational Overhead | Minimal | Observability, tracing, service discovery required |
| Scaling Strategy | Scale vertically + selective feature optimization | Independent service scaling |
| Data Consistency | Easier (shared data layer) | Requires contracts & possibly event-driven patterns |
| Future Evolution | Can be carved into services | Already decomposed |

We will evolve toward **service extraction** only when: (a) a module exhibits distinct scaling characteristics (e.g. embeddings CPU/GPU hot path), (b) independent deploy cadence is needed, or (c) fault isolation materially improves reliability.

## 3. Scalability Strategies

### Caching

- **Vector Retrieval Cache**: Cache results of frequent or recent vector DB queries (e.g., using Redis or in-memory LRU cache).
- **LLM Response Cache**: Cache LLM completions for repeated prompts to avoid unnecessary API calls and reduce cost.
- **Document Chunk Cache**: Cache frequently accessed document chunks in memory for faster retrieval.

### Batching

- **Embedding Batching**: Batch multiple embedding requests to the model API to reduce overhead and improve throughput.
- **LLM Batching**: Where supported, send multiple prompts in a single LLM API call (e.g., OpenAI batch endpoint or local model batch inference).

### Other Patterns

- **Connection Pooling**: Maintain pools for DB and API connections to avoid connection churn.
- **Async/Background Tasks**: Offload long-running or non-critical tasks (e.g., document ingestion, chunking) to background workers.
- **Rate Limiting**: Apply rate limits per user or API key to prevent abuse and ensure fair resource allocation.

## 4. Alternatives Considered

- **Immediate Microservices**: Higher upfront complexity (API contracts, service discovery, distributed tracing). Premature for current traffic and team size.
- **Scale-up Only**: Vertical scaling without architectural optimization leads to cost inefficiency and harder future decomposition.
- **No Caching/Batching**: Simplifies implementation but incurs avoidable latency and cost under repeated queries.
- **Event-Driven Early**: Introducing message brokers now (e.g., Kafka) would add operational burden without clear throughput necessity.

## 5. Consequences

**Pros (Monolith + Layered Enhancements):**

- Faster iteration (single codebase, simpler deployment pipeline).
- Clear refactor path: internal module boundaries become future service APIs.
- Lower operational overhead early; focus on product correctness and performance.
- Caching & batching reduce latency and external API spend.

**Cons / Trade-offs:**

- Risk of growing internal coupling if boundaries aren’t enforced.
- Delayed exposure to distributed system concerns (may be a learning curve later).
- Cache invalidation, eviction policies, and batching heuristics add logic complexity.
- Embedding & LLM hot paths may eventually saturate shared resources, requiring extraction.

**Mitigations:**

- Enforce directory/module boundaries (e.g., `services/`, `routes/`, `core/`).
- Define clear interfaces for future extraction (e.g., embedding service protocol).
- Add metrics & traces early to inform when decomposition is justified.

## 6. Observability & Metrics

- Track cache hit/miss rates for vector and LLM caches.
- Monitor batch sizes, queue times, and throughput for embedding/LLM batching.
- Continue to track latency, error rates, and resource usage (see ADR #2).
- Use tracing to identify bottlenecks in the pipeline.

## 7. Next Steps

Short-Term (Month 2):

- Implement in-memory LRU caches (vector retrieval, LLM responses).
- Introduce batching for embeddings (group small requests within a short window).
- Add metrics: cache hit/miss, batch size distribution, embedding latency percentiles.

Mid-Term (Months 3–6):

- Evaluate Redis for shared caching across replicas.
- Define extraction triggers (e.g., >70% CPU sustained on embeddings module or p95 latency regression after optimization).
- Draft interface spec for a future Embedding Service (request schema, batch semantics).

Long-Term (Beyond Month 6):

- Extract high-intensity modules (embeddings, retrieval) into separate services if justified by metrics.
- Add event streaming only if ingestion throughput or async enrichment drives the need.

Runbooks & Documentation:

- Create cache tuning guide (hit rate targets, memory budget).
- Document batching window strategy (e.g., 20–50ms micro-batch).
- Maintain architectural decision log updates when thresholds trigger reassessment.

---

This ADR will be updated as caching and batching are implemented and evaluated in production-like environments.
