# Architecture Decision Record (ADR Draft)

## Title  

High-Level Architecture for AI Investment Agent v1.0

## Context  

We need a minimal **end-to-end system** to validate design choices early.  
Key drivers:  

- Fast iteration speed.  
- Low setup complexity.  
- Support for AI pipeline (RAG ready).  
- Clear separation between frontend, backend, and data store.  

## Decision  

Adopt a **monolithic FastAPI backend** connected to:  

- **Vector DB** (pgvector/Postgres) for embeddings and similarity search.  
- **LLM provider** (OpenAI/Hugging Face) for Q&A and summarization.  
- **Next.js frontend** for user interaction.  

Architecture will be:  

- **Frontend (Next.js)** → **Backend (FastAPI)** → **Vector DB + LLM**  
- Optional observability/logging layer.  

## Consequences  

**Pros:**  

- Rapid prototyping with minimal moving parts.  
- Leverages Python ecosystem (FastAPI + LangChain compatible).  
- Easy to containerize and deploy locally with Docker Compose.  

**Cons:**  

- Single backend process is a scalability bottleneck.  
- Limited fault isolation (DB/LLM issues may crash API).  
- Observability minimal until later phases.  

**Status:** Accepted for Month 1. To be revisited at ADR #3 (Scaling Strategy).  
