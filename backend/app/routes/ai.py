import asyncio
import time

from fastapi import APIRouter, Depends, Query
from loguru import logger
from opentelemetry import metrics, trace

from app.core.auth import get_api_key
from app.services.ai_service import AIService
from app.services.memory import memory  # in-memory conversation store
from app.services.rag_pipeline import RAGPipeline

# Use global meter provider set in main.py
meter = metrics.get_meter(__name__)
query_time_histogram = meter.create_histogram(
    name="ai_query_time_seconds", description="Time taken to process /query endpoint (seconds)"
)


router = APIRouter(prefix="/ai", tags=["ai"])
ai_service = AIService()
rag_pipeline = RAGPipeline()


# --- /query endpoint ---
from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    conversation_id: str | None = None
    max_history: int | None = 6  # how many previous turns to include


@router.post("/query")
async def query_endpoint(payload: QueryRequest, api_key: str = Depends(get_api_key)):
    """
    Accepts: { "question": "..." }
    Returns: { "answer": "...", "sources": [doc_id, ...], "chunks": [chunk, ...] }
    """
    logger.info(f"/query received: {payload.question}")
    # --- Conversation handling ---
    conversation_id = payload.conversation_id or memory.create_conversation()
    # Append user question to memory early so retrieval can leverage sequence later if needed
    memory.append(conversation_id, "user", payload.question)

    tracer = trace.get_tracer("ai.query")
    start_time = time.time()
    with tracer.start_as_current_span("ai.query") as span:
        span.set_attribute("question.length", len(payload.question))
        span.set_attribute("conversation.id", conversation_id)
        # 1. Embed the question
        with tracer.start_as_current_span("embedding.query"):
            query_embedding = rag_pipeline.embedder.embed_query(payload.question)
        # 2. Retrieve top-k relevant chunks
        top_k = 3
        with tracer.start_as_current_span("retrieval.vector_search") as retrieval_span:
            results = rag_pipeline.vectordb.query_similar(query_embedding, top_k=top_k)
            retrieval_span.set_attribute("retrieval.top_k", top_k)
            retrieval_span.set_attribute("retrieval.result_count", len(results))
        # Each result: (doc_id, chunk_idx, chunk, distance, metadata)
        chunks = [chunk for _, _, chunk, _, _ in results]
        sources = [doc_id for doc_id, _, _, _, _ in results]
        span.set_attribute("sources.count", len(sources))
        # 3. Construct LLM prompt with limited recent history
        history_messages = []
        if payload.max_history and payload.max_history > 0:
            history_messages = memory.last_n(conversation_id, payload.max_history)
        # Exclude the current user question duplication (last message just appended)
        # Format history as role-prefixed lines
        history_block = "\n".join(
            [
                f"{m['role'].upper()}: {m['content']}"
                for m in history_messages[:-1]  # all but newest user question
            ]
        )
        context_text = "\n\n".join(chunks)
        llm_prompt = (
            (f"Conversation History:\n{history_block}\n\n" if history_block else "")
            + f"Context:\n{context_text}\n\nUser Question:\n{payload.question}\n\nYou are an investment research assistant. Provide a clear, concise answer followed by any necessary reasoning."  # guideline
        )
        # 4. Call LLM to get answer (timing handled in AIService, but wrap span for trace linkage)
        with tracer.start_as_current_span("llm.call") as llm_span:
            answer = await ai_service.query_llm(llm_prompt)
            llm_span.set_attribute("llm.prompt.length", len(llm_prompt))
        # 5. Record query time
        duration = time.time() - start_time
        query_time_histogram.record(duration)
        span.set_attribute("query.duration.seconds", duration)
    # 6. Return structured response
    # Append assistant answer to memory
    assistant_answer = answer if not hasattr(answer, "content") else answer.content
    memory.append(conversation_id, "ai", assistant_answer)
    return {
        "answer": assistant_answer,
        "sources": sources,
        "chunks": chunks,
        "conversation_id": conversation_id,
        "history_length": len(memory.get(conversation_id)),
    }


@router.get("/response")
async def get_ai_response(prompt: str, api_key: str = Depends(get_api_key)):
    await asyncio.sleep(0.1)  # simulate I/O
    return {"message": f"Received: {prompt}"}


@router.get("/response-sync")
def ai_response_sync(
    prompt: str = Query(..., description="Prompt for the LLM"), api_key: str = Depends(get_api_key)
):
    import time

    time.sleep(0.1)
    return {"message": f"Received: {prompt}"}
