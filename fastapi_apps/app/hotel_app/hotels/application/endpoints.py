from app.hotel_app.hotels.application.dependencies import get_hotels_service
from fastapi import APIRouter, Query, Depends
from app.hotel_app.hotels.domain.service import HotelsService
from app.hotel_app.hotels.domain.schemas import HotelsOut
from app.hotel_app.hotels.domain.constants import HotelsAttributes
from app.tools.domain.constants import DatabaseQueryOrder
from typing import List, Optional

hotel_router = APIRouter()


@hotel_router.get("/hotels", response_model=List[HotelsOut])
async def get_all_hotels(
    city: Optional[str] = None,
    limit: int = Query(default=100, le=100),
    offset: int = 0,
    order_by: HotelsAttributes = HotelsAttributes.ID,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    rating_gt: float = Query(default=None, le=10),
    rating_lt: float = Query(default=None, ge=0),
    hotels_service: HotelsService = Depends(get_hotels_service),
):
    hotels = await hotels_service.get_all_hotels(
        limit=limit,
        offset=offset,
        order_by=order_by,
        order=order,
        city=city,
        rating_gt=rating_gt,
        rating_lt=rating_lt,
    )
    return hotels
