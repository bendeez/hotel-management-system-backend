from app.tools.domain.base_repository import BaseRepository
from app.hotels.domain.models import Hotels


class HotelsRepository(BaseRepository):
    async def get_all_hotels(self) -> list[Hotels]:
        hotels = await self._get_all(
            model=Hotels,
            relationships=[
                Hotels.hotel_review,
                Hotels.hotel_location,
                Hotels.hotel_rooms,
                Hotels.hotel_house_rules,
                Hotels.hotel_guest_reviews,
            ],
        )
        return hotels
