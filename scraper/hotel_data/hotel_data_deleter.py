from hotel_data.database import SessionLocal
from sqlalchemy import text
import asyncio


async def delete_table(table):
    async with SessionLocal() as db:
        await db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        await db.execute(text(f"TRUNCATE TABLE {table}"))
        await db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        await db.commit()


async def delete_hotel_data():
    tables = [
        "hotels",
        "hotel_review",
        "hotel_rooms",
        "hotel_house_rules",
        "hotel_location",
        "hotel_guest_reviews",
    ]
    tasks = []
    for table in tables:
        tasks.append(delete_table(table))
    await asyncio.gather(*tasks)
