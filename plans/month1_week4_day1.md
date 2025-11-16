Here is your **Month 1, Week 4, Day 1** plan, based on your roadmap and cadence:

---

### **Day 1 — System Design**

**Focus:** Draft complete system diagram.

**Goal:** Visualize the *entire AI Investment Agent v1.0* pipeline, with all components clearly labeled.

**Tasks:**

1. Review prior diagrams (Week 1–3). Merge them into one cohesive architecture:

   * Frontend (Next.js)
   * Backend API (FastAPI)
   * Vector DB (pgvector)
   * Embedding model
   * LLM query and summarization
   * Monitoring (Prometheus + Grafana)
2. Highlight integration boundaries:

   * API–DB
   * DB–LLM
   * API–Frontend
3. Annotate data flow:

   * User → Query → Context retrieval → LLM → Response.
4. Note scaling concerns for tomorrow’s ADR:

   * Components that may split into microservices later.

**Output:**

* `system_diagram_v1.drawio` (or Mermaid diagram)
* Annotated diagram ready for inclusion in **ADR #3 — Scaling Strategy**

---

Would you like a sample **Mermaid or Draw.io-style architecture diagram** template for this day’s output?
