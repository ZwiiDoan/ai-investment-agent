# ai_service.py
# Place your AI service logic here.
import time

import openai
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource

from app.core.settings import settings


meter = metrics.get_meter(__name__)

llm_tokens_counter = meter.create_counter(
    name="ai_llm_tokens_total", description="Total tokens used by LLM in /query endpoint"
)
llm_query_time_histogram = meter.create_histogram(
    name="ai_llm_query_time_seconds",
    description="Time taken for LLM completion in /query endpoint (seconds)",
)


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
            start_time = time.time()
            response = await self.openai_client.chat.completions.create(
                model=self.model, messages=messages
            )
            duration = time.time() - start_time
            llm_query_time_histogram.record(duration)
            # Track tokens if available
            tokens_used = None
            if (
                hasattr(response, "usage")
                and response.usage
                and hasattr(response.usage, "total_tokens")
            ):
                tokens_used = response.usage.total_tokens
                llm_tokens_counter.add(tokens_used)
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            # Handle OpenAI API errors
            raise ValueError(f"OpenAI API error: {e}")
        except Exception as e:
            # Handle network or unexpected errors
            raise ValueError(f"Unexpected error querying LLM: {e}")
