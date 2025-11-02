from fastapi import APIRouter
from datetime import datetime, UTC
from app.core.settings import settings

router = APIRouter(tags=["core"])

@router.get("/")
def root() -> dict:
    return {"message": f"{settings.app_name} is running"}

@router.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "0.1.0", "timestamp": datetime.now(UTC).isoformat()}