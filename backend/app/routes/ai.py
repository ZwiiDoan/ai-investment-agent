import asyncio
from fastapi import APIRouter, Query
from loguru import logger
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])
ai_service = AIService()

@router.get("/ask")
async def ask(prompt: str = Query(..., description="Prompt for the LLM")):
    response = await ai_service.query_llm(prompt)
    logger.info(f"Prompt: {prompt}\nResponse: {response}")
    return {"response": response}

@router.get("/response")
async def get_ai_response(prompt: str):
    await asyncio.sleep(0.1)  # simulate I/O
    return {"message": f"Received: {prompt}"}

@router.get("/response-sync")
def ai_response_sync(prompt: str = Query(..., description="Prompt for the LLM")):
    import time
    time.sleep(0.1)
    return {"message": f"Received: {prompt}"}