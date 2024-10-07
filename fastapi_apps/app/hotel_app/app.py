from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.hotel_app.hotels.application.graphql_endpoint import hotel_router
from app.admin_app.exception_handlers import add_exception_handlers
from tools.application.rate_limiter import limiter

hotel_app = FastAPI()
hotel_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
hotel_app.state.limiter = limiter

add_exception_handlers(app=hotel_app)

hotel_app.include_router(hotel_router)
