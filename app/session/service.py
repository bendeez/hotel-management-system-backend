from app.session.repository import SessionRepository
from fastapi import Depends
from app.tools.constants import DatabaseQueryOrder
from app.session.constants import SessionAttributes
from app.accounts.models import Accounts
from app.session.models import Chat_Sessions
from app.session.schemas import SessionsOut
from app.config import settings
from datetime import timedelta
from uuid import uuid4
from fastapi import Request


class SessionService:
    def __init__(self, repository: SessionRepository = Depends(SessionRepository)):
        self._repository = repository
        self.session_duration = settings.SESSION_DURATION

    async def get_account_chat_sessions(
        self,
        account: Accounts,
        order: DatabaseQueryOrder = DatabaseQueryOrder.DESC,
        order_by: SessionAttributes = SessionAttributes.end_time,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_sessions = await self._repository.get_account_chat_sessions(
            account_id=account.id,
            order=order,
            order_by=order_by,
            limit=limit,
            offset=offset,
        )
        return chat_sessions

    async def create_chat_session(self, account: Accounts, request: Request):
        session = await self._repository.create(
            model_instance=Chat_Sessions(
                id=str(uuid4()),
                account_id=account.id,
                ip_address=request.client.host,
                user_agent=request.headers.get("User-Agent"),
            )
        )
        return session
