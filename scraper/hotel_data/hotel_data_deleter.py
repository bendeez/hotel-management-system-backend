from hotel_data.database import SessionLocal
from sqlalchemy import text


async def delete_hotel_data():
    async with SessionLocal() as db:
        await db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        await db.execute(text("TRUNCATE TABLE hotels"))
        await db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        await db.commit()
