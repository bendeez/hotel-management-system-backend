from apps.scraper.hotel_data.models import Hotels
from apps.scraper.hotel_data.database import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import asyncio


async def get_hotel_data() -> list[Hotels]:
    async with SessionLocal() as db:
        hotel_data = await db.execute(
            select(Hotels)
            .options(
                selectinload(Hotels.hotel_rooms),
                selectinload(Hotels.hotel_review),
                selectinload(Hotels.hotel_location),
                selectinload(Hotels.hotel_guest_reviews),
                selectinload(Hotels.hotel_house_rules),
            )
            .order_by(Hotels.title)
        )
        hotel_data = hotel_data.scalars().all()
        return hotel_data


if __name__ == "__main__":
    asyncio.run(get_hotel_data())
