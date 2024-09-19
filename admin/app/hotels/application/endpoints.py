from app.hotels.application.dependencies import get_hotels_service
from fastapi import APIRouter, Depends
from app.hotels.domain.service import HotelsService
from app.hotels.domain.schemas import HotelsOut
from typing import List

hotels_router = APIRouter()


@hotels_router.get("/hotels", response_model=List[HotelsOut])
async def get_all_hotels(hotels_service: HotelsService = Depends(get_hotels_service)):
    hotels = await hotels_service.get_all_hotels()
    return hotels
