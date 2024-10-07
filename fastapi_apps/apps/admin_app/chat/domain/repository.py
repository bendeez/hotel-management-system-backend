from apps.admin_app.chat.domain.constants import ChatsAttributes
from tools.domain.constants import DatabaseQueryOrder
from apps.admin_app.chat.domain.models import Chat_Logs
from apps.admin_app.session.domain.repository import SessionRepository
from apps.admin_app.accounts.domain.models import Accounts
from tools.domain.base_repository import JoinExpression
from sqlalchemy.sql.elements import BinaryExpression


class ChatRepository(SessionRepository):
    async def get_all_account_chat_logs(
        self,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        limit: int,
        offset: int,
        account_id: int,
        extra_filters: list[BinaryExpression],
    ) -> list[Chat_Logs]:
        filters = [Accounts.id == account_id] + extra_filters
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
