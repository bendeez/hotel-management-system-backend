from app.hotel_app.application.dependencies import get_hotels_service
from fastapi import FastAPI, Query, Depends
from app.hotel_app.domain.service import HotelsService
from app.hotel_app.domain.schemas import HotelsOut
from app.hotel_app.domain.constants import HotelsAttributes
from app.tools.domain.constants import DatabaseQueryOrder
from typing import List, Optional

hotel_app = FastAPI()


@hotel_app.get("/hotels", response_model=List[HotelsOut])
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
