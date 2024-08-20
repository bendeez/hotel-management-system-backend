from fastapi import APIRouter, Depends
from app.session.schemas import SessionsOut
from app.session.constants import SessionAttributes
from app.tools.constants import DatabaseQueryOrder
from app.session.repository import SessionRepository
from typing import List

session_router = APIRouter()


@session_router.get("/sessions", response_model=List[SessionsOut])
async def get_chat_sessions(
    limit: int = 100,
    offset: int = 0,
    order_by: SessionAttributes = SessionAttributes.end_time,
    order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
    session_repository: SessionRepository = Depends(SessionRepository),
):
    chat_sessions = await session_repository.get_chat_sessions(
        limit=limit, offset=offset, order=order, order_by=order_by
    )
    return chat_sessions
