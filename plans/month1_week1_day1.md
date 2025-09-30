# Month 1 → Week 1 → Day 1: High-Level System Design

## Goal  

Capture the **big-picture architecture** of the AI Investment Agent to anchor later implementation.

## Steps  

1. **Define user flow:**  
   - User (web browser or mobile)  
   - → Frontend (Next.js)  
   - → Backend API (FastAPI)  
   - → Vector DB (for context storage & retrieval)  
   - → LLM (OpenAI/HuggingFace)  
   - → Response back to frontend  

2. **Draw a simple component diagram** with these elements:  
   - **Frontend (Next.js):** Input + results UI.  
   - **Backend (FastAPI):** REST API, orchestrates flow.  
   - **Vector DB (pgvector / Pinecone):** Stores embeddings for RAG.  
   - **LLM Service:** Provides AI reasoning and summarization.  
   - **External Data (News/Docs):** Optional ingestion later.  

3. **Capture in ADR** (Architecture Decision Record draft):  
   - Title: *High-Level Architecture for AI Investment Agent v1.0*  
   - Context: Need minimal end-to-end system to test flows early.  
   - Decision: Start with monolith (FastAPI + Vector DB + LLM) behind one API.  
   - Consequences: Quick iteration, limited scalability (acceptable for Month 1).  
