from fastapi import Depends
from app.hotel_app.domain.repository import HotelsRepository
from app.hotel_app.domain.service import HotelsService
from app.tools.application.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def _get_hotels_repository(db: AsyncSession = Depends(get_db)) -> HotelsRepository:
    return HotelsRepository(db=db)


def get_hotels_service(
    hotels_repository: HotelsRepository = Depends(_get_hotels_repository),
) -> HotelsService:
    return HotelsService(repository=hotels_repository)
