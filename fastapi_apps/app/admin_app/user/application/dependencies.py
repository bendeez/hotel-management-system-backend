from app.admin_app.user.domain.repository import UserRepository
from app.admin_app.user.domain.service import UserService
from tools.application.dependencies import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def _get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db)


def get_user_service(
    user_repository: UserRepository = Depends(_get_user_repository),
) -> UserService:
    return UserService(repository=user_repository)
