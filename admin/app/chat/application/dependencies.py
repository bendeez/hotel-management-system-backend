from fastapi import Depends
from app.chat.domain.repository import ChatRepository
from app.chat.domain.service import ChatService
from app.tools.application.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def get_chat_repository(db: AsyncSession = Depends(get_db)) -> ChatRepository:
    return ChatRepository(db=db)


def get_chat_service(
    chat_repository: ChatRepository = Depends(get_chat_repository),
) -> ChatService:
    return ChatService(repository=chat_repository)
