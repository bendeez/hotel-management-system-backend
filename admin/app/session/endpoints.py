from fastapi import APIRouter, Depends, Request, status
from admin.app.session.schemas import SessionsOut
from admin.app.session.constants import SessionAttributes
from admin.app.tools.constants import DatabaseQueryOrder
from admin.app.session.service import SessionService
from typing import List
from admin.app.accounts.models import Accounts
from admin.app.auth.service import get_account
from admin.app.tools.rate_limiter import limiter, limit

session_router = APIRouter()


@session_router.get("/sessions", response_model=List[SessionsOut])
@limiter.limit(limit)
async def get_chat_sessions(
    request: Request,
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
@limiter.limit(limit)
async def create_chat_session(
    request: Request,
    session_service: SessionService = Depends(SessionService),
    account: Accounts = Depends(get_account),
):
    session = await session_service.create_chat_session(
        account=account, request=request
    )
    return session
