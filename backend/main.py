import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.error_handlers import register_exception_handlers
from app.core.middleware.logging import log_requests

# Project-specific imports
from app.core.settings import settings
from app.core.telemetry import setup_otel
from app.routes.ai import router as ai_router
from app.routes.core import router as core_router
from app.routes.documents import router as documents_router

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

# OpenTelemetry setup (metrics, tracing, exporter)
setup_otel(app)

# Register routers
app.include_router(documents_router)
app.include_router(core_router)
app.include_router(ai_router)

# Enhanced structured logging middleware
app.middleware("http")(log_requests)
