from fastapi import APIRouter, Depends, status, Request
from admin.app.chat.service import ChatService
from admin.app.chat.constants import ChatsAttributes
from admin.app.tools.constants import DatabaseQueryOrder
from admin.app.chat.schemas import ChatLogsOut, ChatLogsCreate
from admin.app.accounts.models import Accounts
from admin.app.auth.service import get_account
from typing import List
from admin.app.tools.rate_limiter import limiter, limit

chat_router = APIRouter()


@chat_router.get("/chat-logs", response_model=List[ChatLogsOut])
@limiter.limit(limit)
async def get_all_account_chat_logs(
    request: Request,
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
@limiter.limit(limit)
async def get_account_chat_logs_by_session_id(
    request: Request,
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


@chat_router.post(
    "/chat-log", response_model=ChatLogsOut, status_code=status.HTTP_201_CREATED
)
@limiter.limit(limit)
async def create_chat_log(
    request: Request,
    chat_log: ChatLogsCreate,
    chat_service: ChatService = Depends(ChatService),
    account: Accounts = Depends(get_account),
):
    chat_log = await chat_service.create_chat_log(account=account, chat_log=chat_log)
    return chat_log


@chat_router.delete("/chat-log/{chat_log_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(limit)
async def delete_chat_log(
    request: Request,
    chat_log_id: int,
    chat_service: ChatService = Depends(ChatService),
    account: Accounts = Depends(get_account),
):
    await chat_service.delete_chat_log(chat_log_id=chat_log_id, account=account)
