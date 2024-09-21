from app.hotels.application.dependencies import get_hotels_service
from fastapi import APIRouter, Depends, Query
from app.hotels.domain.service import HotelsService
from app.hotels.domain.schemas import HotelsOut
from app.hotels.domain.constants import HotelsAttributes
from app.tools.domain.constants import DatabaseQueryOrder
from typing import List, Optional

hotels_router = APIRouter()


@hotels_router.get("/hotels", response_model=List[HotelsOut])
async def get_all_hotels(
    city: Optional[str] = None,
    limit: int = Query(default=100, le=100),
    offset: int = 0,
    order_by: HotelsAttributes = HotelsAttributes.ID,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    hotels_service: HotelsService = Depends(get_hotels_service),
):
    hotels = await hotels_service.get_all_hotels(
        limit=limit, offset=offset, order_by=order_by, order=order, city=city
    )
    return hotels
