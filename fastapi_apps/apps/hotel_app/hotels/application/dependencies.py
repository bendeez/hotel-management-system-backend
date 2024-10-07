from fastapi import Depends
from apps.hotel_app.hotels.domain.repository import HotelsRepository
from apps.hotel_app.hotels.domain.service import HotelsService
from tools.application.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def _get_hotels_repository(db: AsyncSession = Depends(get_db)) -> HotelsRepository:
    return HotelsRepository(db=db)


def get_hotels_service(
    hotels_repository: HotelsRepository = Depends(_get_hotels_repository),
) -> HotelsService:
    return HotelsService(repository=hotels_repository)
