from sqlalchemy.orm.attributes import InstrumentedAttribute
from fastapi import Depends
from app.tools.db.database import get_db
from app.tools.enums import DatabaseQueryOrder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc
from typing import Optional, Any


class DatabaseTransactionService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, model, **attributes):
        model_instance = model(**attributes)
        self.db.add(model_instance)
        await self.db.commit()
        await self.db.refresh(model_instance)
        return model_instance

    async def delete(self, model_instance, ongoing_transaction=False):
        await self.db.delete(model_instance)
        if not ongoing_transaction:
            await self.db.commit()

    async def get_all(
        self,
        model,
        filter: Optional[dict[InstrumentedAttribute, Any]] = {},
        order_by: Optional[InstrumentedAttribute] = None,
        order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
        limit: int = 100,
        offset: int = 100,
    ):
        order_by = desc(order_by) if order == DatabaseQueryOrder.DESC else asc(order_by)
        stmt = (
            select(model)
            .order_by(order_by)
            .limit(limit)
            .offset(offset)
            .where(*[attribute == value for attribute, value in filter.items()])
        )
        models = await self.db.execute(stmt)
        return models.scalars().all()

    async def get_one(self, model, filter: Optional[dict] = None):
        stmt = select(model)
        if filter is not None:
            stmt = stmt.where(
                *[attribute == value for attribute, value in filter.items()]
            )
        model = await self.db.execute(stmt)
        return model.scalars().first()
