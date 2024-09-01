from fastapi import APIRouter, Depends, Request, status
from app.session.schemas import SessionsOut
from app.session.constants import SessionAttributes
from app.tools.constants import DatabaseQueryOrder
from app.session.service import SessionService
from typing import List
from app.accounts.models import Accounts
from app.auth.service import get_account

session_router = APIRouter(prefix="/session")


@session_router.get("/sessions", response_model=List[SessionsOut])
async def get_chat_sessions(
    limit: int = 100,
    offset: int = 0,
    order_by: SessionAttributes = SessionAttributes.end_time,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    session_service: SessionService = Depends(SessionService),
    account: Accounts = Depends(get_account),
):
    chat_sessions = await session_service.get_account_chat_sessions(
        account=account, limit=limit, offset=offset, order=order, order_by=order_by
    )
    return chat_sessions


@session_router.post(
    "/session", response_model=SessionsOut, status_code=status.HTTP_201_CREATED
)
async def create_chat_session(
    request: Request,
    session_service: SessionService = Depends(SessionService),
    account: Accounts = Depends(get_account),
):
    session = await session_service.create_chat_session(
        account=account, request=request
    )
    return session
