**Month 1 – Week 1 – Day 3: AI Integration (1h)**

### Goal

Connect FastAPI backend to an LLM provider to complete the minimal AI response flow.

---

### Tasks

1. **Set Up API Keys:**

   * Obtain and store your OpenAI or Hugging Face API key in `.env`.
   * Add it to FastAPI settings via `pydantic.BaseSettings`.

2. **Create Service Module:**

   * Implement `ai_service.py` with a function `query_llm(prompt: str) -> str`.
   * Use `httpx` or `requests` for async API calls.

   ```python
   import httpx
   from pydantic import BaseSettings

   class Settings(BaseSettings):
       openai_api_key: str
       model: str = "gpt-4o-mini"

   settings = Settings()

   async def query_llm(prompt: str):
       headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
       payload = {"model": settings.model, "messages": [{"role": "user", "content": prompt}]}
       async with httpx.AsyncClient() as client:
           res = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
           return res.json()["choices"][0]["message"]["content"]
   ```

3. **Expose Endpoint:**
   Add a FastAPI route `/ask` to call `query_llm()` and return the result.

   ```python
   from fastapi import FastAPI
   from ai_service import query_llm

   app = FastAPI()

   @app.get("/ask")
   async def ask(prompt: str):
       return {"response": await query_llm(prompt)}
   ```

4. **Test Locally:**

   * Run `uvicorn main:app --reload`.
   * Visit `http://127.0.0.1:8000/ask?prompt=Hello`.

5. **Verify Flow:**

   * Ensure you receive a valid LLM-generated message.
   * Log both prompt and response to console for now.

---

### Output

* FastAPI + LLM working endpoint (`/ask`).
* Verified local call and response.
* Notes for ADR #1 (*Why Python + FastAPI as base stack*).
