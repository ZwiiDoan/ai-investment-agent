from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from app.core.settings import settings

# Name of the header clients must use
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

VALID_API_KEY = settings.x_api_key


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == VALID_API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
        headers={"WWW-Authenticate": "API Key"},
    )
