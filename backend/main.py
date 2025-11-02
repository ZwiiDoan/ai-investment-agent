from prometheus_fastapi_instrumentator import Instrumentator

import os
import time
import uuid
import json
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.error_handlers import register_exception_handlers
from app.core.settings import settings


from app.routes.documents import router as documents_router
from app.routes.core import router as core_router
from app.routes.ai import router as ai_router

app = FastAPI(title=settings.app_name)
register_exception_handlers(app)
allowed_origins = [
    origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("logs", exist_ok=True)
logger.add("logs/app.log", rotation="1 week", serialize=True)  # JSON logs

# Prometheus metrics instrumentation
Instrumentator().instrument(app).expose(app)

# Register routers
app.include_router(documents_router)
app.include_router(core_router)
app.include_router(ai_router)

# Structured logging middleware with request ID, endpoint, latency, and status
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    response: Response = await call_next(request)
    duration = time.time() - start_time
    log_data = {
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "latency": round(duration, 4),
        "client_host": request.client.host if request.client else None,
    }
    logger.info(json.dumps(log_data))
    response.headers["X-Request-ID"] = request_id
    return response