from app.user.domain.repository import UserRepository
from app.user.domain.service import UserService
from app.tools.application.dependencies import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository=user_repository)
