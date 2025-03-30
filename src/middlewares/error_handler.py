from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error"},
            )


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )



logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.critical(f"Unhandled Exception: {exc}", exc_info=True)  
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error"},
            )
