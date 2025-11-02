# ai_service.py
# Place your AI service logic here.


import openai

from app.core.settings import settings


class AIService:
    def __init__(self):
        self.app_name = settings.app_name
        self.version = "0.1.0"
        self.openai_api_key = settings.openai_api_key
        self.model = settings.model
        self.openai_client = openai.AsyncOpenAI(api_key=self.openai_api_key)

    async def query_llm(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI investment assistant.",
        history: list = None,
    ) -> str:
        """
        Query the LLM with a structured prompt and handle errors robustly.
        Args:
            prompt: The user's message.
            system_prompt: The system message for context.
            history: Optional list of previous messages (dicts with 'role' and 'content').
        Returns:
            The LLM's response as a string.
        Raises:
            ValueError: If API key is missing or OpenAI returns an error.
        """
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not set in environment/settings.")

        # Build structured messages
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model, messages=messages
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            # Handle OpenAI API errors
            raise ValueError(f"OpenAI API error: {e}")
        except Exception as e:
            # Handle network or unexpected errors
            raise ValueError(f"Unexpected error querying LLM: {e}")
