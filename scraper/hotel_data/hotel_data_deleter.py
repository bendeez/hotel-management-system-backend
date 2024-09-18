from hotel_data.models import (
    Hotels,
    Hotel_Rooms,
    Hotel_Location,
    Hotel_Review,
    Hotel_Guest_Reviews,
    Hotel_House_Rules,
)
from hotel_data.database import SessionLocal
import asyncio
from sqlalchemy import delete


async def delete_hotel_data():
    async with SessionLocal() as db:
        """
            put hotels table at end of list so
            it is deleted last after the foreign
            key references have been deleted
        """
        for table in [
            Hotel_Rooms,
            Hotel_Location,
            Hotel_Review,
            Hotel_Guest_Reviews,
            Hotel_House_Rules,
            Hotels,
        ]:
            await db.execute(delete(table))
        await db.commit()


if __name__ == "__main__":
    asyncio.run(delete_hotel_data())
