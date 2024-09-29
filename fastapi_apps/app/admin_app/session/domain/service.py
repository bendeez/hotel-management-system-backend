from app.admin_app.session.domain.repository import SessionRepository
from app.tools.domain.constants import DatabaseQueryOrder
from app.admin_app.session.domain.constants import SessionAttributes
from app.admin_app.accounts.domain.models import Accounts
from app.admin_app.session.domain.models import Chat_Sessions
from app.config import settings
from uuid import uuid4
from fastapi import Request


class SessionService:
    def __init__(self, repository: SessionRepository):
        self._repository = repository
        self.session_duration = settings.SESSION_DURATION

    async def get_account_chat_sessions(
        self,
        account: Accounts,
        order: DatabaseQueryOrder,
        order_by: SessionAttributes,
        limit: int,
        offset: int,
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
