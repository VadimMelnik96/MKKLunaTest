from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.exceptions.exceptions import NotFoundError


async def validation_exception_handler(
        request: Request, exception: RequestValidationError
) -> JSONResponse:
    """Обработчик ошибки валидации"""
    errors = exception.errors()

    for error in errors:
        if "ctx" in error:
            for key, value in error["ctx"].items():
                if isinstance(value, Exception):
                    error["ctx"][key] = str(value)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors},
    )


async def not_found_exception_handler(request: Request, exception: NotFoundError) -> JSONResponse:
    """Обработчик NotFoundError"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Not found error"},
    )

exception_config = {
    RequestValidationError: validation_exception_handler,
    NotFoundError: not_found_exception_handler,
}