from fastapi import FastAPI
from app.hotel_app.hotels.application.endpoints import hotel_router

hotel_app = FastAPI()

hotel_app.include_router(hotel_router)
