from fastapi import APIRouter, Depends, Request, status
from app.session.domain.schemas import SessionsOut
from app.session.domain.constants import SessionAttributes
from app.tools.domain.constants import DatabaseQueryOrder
from app.session.domain.service import SessionService
from app.session.application.dependencies import get_session_service
from typing import List
from app.accounts.domain.models import Accounts
from app.auth.application.dependencies import get_account
from app.tools.application.rate_limiter import limiter, limit

session_router = APIRouter()


@session_router.get("/sessions", response_model=List[SessionsOut])
@limiter.limit(limit)
async def get_chat_sessions(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    order_by: SessionAttributes = SessionAttributes.END_TIME,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    session_service: SessionService = Depends(get_session_service),
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
    session_service: SessionService = Depends(get_session_service),
    account: Accounts = Depends(get_account),
):
    session = await session_service.create_chat_session(
        account=account, request=request
    )
    return session
