from fastapi import APIRouter, Depends
from app.chat.service import ChatService
from app.chat.constants import ChatsAttributes
from app.tools.constants import DatabaseQueryOrder
from app.chat.schemas import ChatLogsOut, ChatLogsCreate
from app.accounts.models import Accounts
from app.auth.service import get_account
from typing import List

chat_router = APIRouter(prefix="/chat")


@chat_router.get("/chat-logs", response_model=List[ChatLogsOut])
async def get_all_account_chat_logs(
    limit: int = 100,
    offset: int = 0,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    order_by: ChatsAttributes = ChatsAttributes.date,
    chat_service: ChatService = Depends(ChatService),
    account: Accounts = Depends(get_account),
):
    chat_logs = await chat_service.get_all_account_chat_logs(
        order=order, order_by=order_by, limit=limit, offset=offset, account=account
    )
    return chat_logs


@chat_router.get("/chat-logs/{session_id}", response_model=List[ChatLogsOut])
async def get_account_chat_logs_by_session_id(
    session_id: str,
    limit: int = 100,
    offset: int = 0,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    order_by: ChatsAttributes = ChatsAttributes.date,
    chat_service: ChatService = Depends(ChatService),
    account: Accounts = Depends(get_account),
):
    chat_logs = await chat_service.get_chat_logs_by_session_id(
        order=order,
        order_by=order_by,
        limit=limit,
        session_id=session_id,
        offset=offset,
        account=account,
    )
    return chat_logs


@chat_router.post("/chat-log", response_model=ChatLogsOut)
async def create_chat_log(
    chat_log: ChatLogsCreate,
    chat_service: ChatService = Depends(ChatService),
    account: Accounts = Depends(get_account),
):
    chat_log = await chat_service.create_chat_log(account=account, chat_log=chat_log)
    return chat_log
