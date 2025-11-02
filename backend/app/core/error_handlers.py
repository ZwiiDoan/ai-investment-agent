from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


def register_exception_handlers(app):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500, content={"error": "Internal server error. Please try again later."}
        )
