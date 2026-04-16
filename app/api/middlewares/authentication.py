from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Аутентификационный middleware"""

    def __init__(self, app: FastAPI, api_key: str, exclude_paths: set[str]| None = None):
        super().__init__(app)
        self.api_key = api_key
        self.exclude_paths = exclude_paths or set()

    async def dispatch(self, request: Request, call_next):          # noqa: ANN001, ANN201
        """Проверка апи-ключа"""
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if api_key != self.api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API key"},
            )

        return await call_next(request)

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)
