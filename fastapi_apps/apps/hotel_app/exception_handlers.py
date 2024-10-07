from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apps.hotel_app.exceptions import HotelError
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


async def hotel_exception_handler(request: Request, exc: HotelError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.message},
        headers=exc.headers,
    )


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HotelError, hotel_exception_handler)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
