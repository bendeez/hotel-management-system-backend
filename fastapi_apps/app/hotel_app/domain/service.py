from app.hotel_app.domain.repository import HotelsRepository
from app.tools.domain.constants import DatabaseQueryOrder
from app.hotel_app.domain.constants import HotelsAttributes
from typing import Optional


class HotelsService:
    def __init__(self, repository: HotelsRepository):
        self.repository = repository

    async def get_all_hotels(
        self,
        limit: int,
        offset: int,
        order: DatabaseQueryOrder,
        order_by: HotelsAttributes,
        city: Optional[str] = None,
    ):
        hotels = await self.repository.get_all_hotels(
            limit=limit, offset=offset, order=order, order_by=order_by, city=city
        )
        return hotels
