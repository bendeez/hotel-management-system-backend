from fastapi import APIRouter, Depends
from app.chat.service import ChatService
from app.chat.enums import ChatsAttributes, SessionAttributes
from app.tools.enums import DatabaseQueryOrder
from app.chat.schemas import ChatLogsOut, SessionsOut
from typing import List

chat_logs_router = APIRouter(prefix="/chat")


@chat_logs_router.get("/chat-logs", response_model=List[ChatLogsOut])
async def get_all_chat_logs(
    limit: int = 100,
    offset: int = 0,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    order_by: ChatsAttributes = ChatsAttributes.date,
    chat: ChatService = Depends(ChatService),
):
    chat_logs = await chat.get_all_chat_logs(
        order=order, order_by=order_by, limit=limit, offset=offset
    )
    return chat_logs


@chat_logs_router.get("/chat-logs/{session_id}", response_model=List[ChatLogsOut])
async def get_chat_logs_by_session_id(
    session_id: str,
    limit: int = 100,
    offset: int = 0,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    order_by: ChatsAttributes = ChatsAttributes.date,
    chat: ChatService = Depends(ChatService),
):
    chat_logs = await chat.get_chat_logs_by_session_id(
        order=order,
        order_by=order_by,
        limit=limit,
        session_id=session_id,
        offset=offset,
    )
    return chat_logs


@chat_logs_router.get("/sessions", response_model=List[SessionsOut])
async def get_chat_sessions(
    limit: int = 100,
    offset: int = 0,
    order_by: SessionAttributes = SessionAttributes.expiry,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    chat_logs_service: ChatService = Depends(ChatService),
):
    chat_sessions = await chat_logs_service.get_chat_sessions(
        limit=limit, offset=offset, order=order, order_by=order_by
    )
    return chat_sessions
