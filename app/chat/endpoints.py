from fastapi import APIRouter, Depends
from app.chat.repository import ChatRepository
from app.chat.constants import ChatsAttributes
from app.tools.constants import DatabaseQueryOrder
from app.chat.schemas import ChatLogsOut
from typing import List

chat_router = APIRouter(prefix="/chat")


@chat_router.get("/chat-logs", response_model=List[ChatLogsOut])
async def get_all_chat_logs(
    limit: int = 100,
    offset: int = 0,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    order_by: ChatsAttributes = ChatsAttributes.date,
    chat_repository: ChatRepository = Depends(ChatRepository),
):
    chat_logs = await chat_repository.get_all_chat_logs(
        order=order, order_by=order_by, limit=limit, offset=offset
    )
    return chat_logs


@chat_router.get("/chat-logs/{session_id}", response_model=List[ChatLogsOut])
async def get_chat_logs_by_session_id(
    session_id: str,
    limit: int = 100,
    offset: int = 0,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    order_by: ChatsAttributes = ChatsAttributes.date,
    chat_repository: ChatRepository = Depends(ChatRepository),
):
    chat_logs = await chat_repository.get_chat_logs_by_session_id(
        order=order,
        order_by=order_by,
        limit=limit,
        session_id=session_id,
        offset=offset,
    )
    return chat_logs
