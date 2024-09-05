from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from admin.app.exceptions import AdminError
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


async def admin_exception_handler(request: Request, exc: AdminError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.message},
        headers=exc.headers,
    )


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AdminError, admin_exception_handler)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
