from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import selectinload, with_polymorphic
from fastapi import Depends
from app.tools.database import get_db
from app.tools.constants import DatabaseQueryOrder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc, inspect
from typing import Optional, Any


class BaseRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, model_instance, ongoing_transaction=False):
        self.db.add(model_instance)
        if not ongoing_transaction:
            await self.db.commit()
            await self.db.refresh(model_instance)
        return model_instance

    async def delete(self, model_instance, ongoing_transaction=False):
        await self.db.delete(model_instance)
        if not ongoing_transaction:
            await self.db.commit()

    def _build_query(
        self,
        model,
        polymorphic: bool = False,
        filter: Optional[dict[InstrumentedAttribute, Any]] = None,
        relationships: Optional[list[InstrumentedAttribute]] = None,
    ):
        filter = filter or {}
        relationships = relationships or []
        if polymorphic:
            model = with_polymorphic(model, "*")
        stmt = (
            select(model)
            .where(*[attribute == value for attribute, value in filter.items()])
            .options(
                *[selectinload(relationship) for relationship in relationships]
            )  # no chaining
        )
        return stmt

    async def _get_all(
        self,
        model,
        polymorphic: bool = False,
        filter: Optional[dict[InstrumentedAttribute, Any]] = None,
        relationships: Optional[list[InstrumentedAttribute]] = None,
        order_by: Optional[InstrumentedAttribute] = None,
        order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
        limit: int = 100,
        offset: int = 0,
    ):
        order_by = order_by or inspect(model).primary_key[0]
        order_by = desc(order_by) if order == DatabaseQueryOrder.DESC else asc(order_by)
        stmt = self._build_query(
            model=model,
            polymorphic=polymorphic,
            filter=filter,
            relationships=relationships,
        )
        stmt = stmt.order_by(order_by).limit(limit).offset(offset)
        model_instances = await self.db.execute(stmt)
        return model_instances.scalars().all()

    async def _get_one(
        self,
        model,
        polymorphic: bool = False,
        filter: Optional[dict[InstrumentedAttribute, Any]] = None,
        relationships: Optional[list[InstrumentedAttribute]] = None,
    ):
        stmt = self._build_query(
            model=model,
            polymorphic=polymorphic,
            filter=filter,
            relationships=relationships,
        )
        model_instance = await self.db.execute(stmt)
        return model_instance.scalars().first()
