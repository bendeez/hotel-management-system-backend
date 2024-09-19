from app.hotels.domain.repository import HotelsRepository


class HotelsService:
    def __init__(self, repository: HotelsRepository):
        self.repository = repository

    async def get_all_hotels(self):
        hotels = await self.repository.get_all_hotels()
        return hotels
