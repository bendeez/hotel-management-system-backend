from hotel_data.models import (
    Hotels,
    Hotel_Rooms,
    Hotel_Location,
    Hotel_Review,
    Hotel_Guest_Reviews,
    Hotel_House_Rules,
)
from hotel_data.database import SessionLocal
from sqlalchemy import delete
import asyncio


async def delete_specific_hotel_table(table):
    async with SessionLocal() as db:
        """
            put hotels table at end of list so
            it is deleted last after the foreign
            key references have been deleted
        """

        await db.execute(delete(table))
        await db.commit()


async def delete_hotel_data():
    tasks = []
    for table in [
        Hotel_Rooms,
        Hotel_Location,
        Hotel_Review,
        Hotel_Guest_Reviews,
        Hotel_House_Rules,
        Hotels,
    ]:
        tasks.append(delete_specific_hotel_table(table))
    await asyncio.gather(*tasks)
