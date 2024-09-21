from app.hotels.domain.repository import HotelsRepository
from app.tools.domain.constants import DatabaseQueryOrder
from app.hotels.domain.constants import HotelsAttributes


class HotelsService:
    def __init__(self, repository: HotelsRepository):
        self.repository = repository

    async def get_all_hotels(
        self,
        limit: int,
        offset: int,
        order: DatabaseQueryOrder,
        order_by: HotelsAttributes,
    ):
        hotels = await self.repository.get_all_hotels(
            limit=limit, offset=offset, order=order, order_by=order_by
        )
        return hotels
