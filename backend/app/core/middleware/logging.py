import json
import time
import uuid
from fastapi import Request, Response
from opentelemetry.trace import get_current_span
from loguru import logger


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
