from app.admin_app.chat.domain.constants import ChatsAttributes
from app.tools.domain.constants import DatabaseQueryOrder
from app.admin_app.chat.domain.models import Chat_Logs
from app.admin_app.session.domain.repository import SessionRepository
from app.admin_app.accounts.domain.models import Accounts
from app.tools.domain.base_repository import JoinExpression
from typing import Optional


class ChatRepository(SessionRepository):
    async def get_all_account_chat_logs(
        self,
        account_id: int,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        limit: int,
        offset: int,
        session_id: Optional[str] = None,
    ) -> list[Chat_Logs]:
        filters = [Accounts.id == account_id]
        if session_id is not None:
            filters.append(Chat_Logs.session_id == session_id)
        chat_logs = await self._get_all(
            model=Chat_Logs,
            order_by=getattr(Chat_Logs, order_by.value),
            order=order,
            offset=offset,
            limit=limit,
            joins=[JoinExpression(model=Chat_Logs.account)],
            filters=filters,
        )
        return chat_logs

    async def get_account_chat_log_by_id(
        self, account_id: int, chat_log_id: int
    ) -> Chat_Logs:
        chat_log = await self._get_one(
            model=Chat_Logs,
            joins=[JoinExpression(model=Chat_Logs.account)],
            filters=[Accounts.id == account_id, Chat_Logs.id == chat_log_id],
        )
        return chat_log