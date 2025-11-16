import json
import os
import time
import uuid

import structlog
from fastapi import Request, Response
from loguru import logger
from opentelemetry.trace import get_current_span
from starlette.middleware.base import BaseHTTPMiddleware


def setup_structlog():
    import structlog

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(10),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


class RequestIdUserIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate or extract request_id
        request_id = request.headers.get("X-Request-Id") or os.urandom(8).hex()
        # Extract user_id if present (could be from auth or header)
        user_id = request.headers.get("X-User-Id", "anonymous")
        # Bind to structlog context for this request
        structlog.contextvars.bind_contextvars(request_id=request_id, user_id=user_id)
        response = await call_next(request)
        # Unbind after request
        structlog.contextvars.clear_contextvars()
        return response


async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    # Try to extract user_id from headers or query params (if present)
    user_id = request.headers.get("X-User-ID") or request.query_params.get("user_id")
    # Try to extract top_k, tokens_in, tokens_out, retrieved_doc_ids from request body (if present)
    try:
        body = await request.json()
    except Exception:
        body = {}
    top_k = body.get("top_k")
    tokens_in = body.get("tokens_in")
    tokens_out = body.get("tokens_out")
    retrieved_doc_ids = body.get("retrieved_doc_ids")
    # Route name (endpoint function name)
    route_name = None
    if hasattr(request, "scope") and "endpoint" in request.scope:
        route_name = getattr(request.scope["endpoint"], "__name__", None)
    response: Response = await call_next(request)
    duration_ms = int((time.time() - start_time) * 1000)
    log_data = {
        "req_id": request_id,
        "route": route_name or request.url.path,
        "method": request.method,
        "user_id": user_id,
        "latency_ms": duration_ms,
        "status": response.status_code,
        "client_host": request.client.host if request.client else None,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "top_k": top_k,
        "retrieved_doc_ids": retrieved_doc_ids,
        "trace_id": (
            format(get_current_span().get_span_context().trace_id, "032x")
            if get_current_span()
            else None
        ),
    }
    logger.info(json.dumps(log_data))
    response.headers["X-Request-ID"] = request_id
    return response
