from app.session.domain.repository import SessionRepository
from app.session.domain.service import SessionService
from app.tools.application.dependencies import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_session_repository(db: AsyncSession = Depends(get_db)) -> SessionRepository:
    return SessionRepository(db=db)


def get_session_service(
    session_repository: SessionRepository = Depends(get_session_repository),
) -> SessionService:
    return SessionService(repository=session_repository)
