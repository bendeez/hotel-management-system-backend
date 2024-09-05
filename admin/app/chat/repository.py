from admin.app.chat.constants import ChatsAttributes
from admin.app.tools.constants import DatabaseQueryOrder
from admin.app.chat.models import Chat_Logs
from admin.app.session.repository import SessionRepository
from admin.app.accounts.models import Accounts
from admin.app.tools.base_repository import JoinExpression


class ChatRepository(SessionRepository):
    async def get_all_account_chat_logs(
        self,
        account_id: int,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_logs = await self._get_all(
            model=Chat_Logs,
            order_by=getattr(Chat_Logs, order_by.value),
            order=order,
            offset=offset,
            limit=limit,
            joins=[JoinExpression(model=Chat_Logs.account)],
            filters=[Accounts.id == account_id],
        )
        return chat_logs

    async def get_account_chat_logs_by_session_id(
        self,
        account_id: int,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_logs = await self._get_all(
            model=Chat_Logs,
            order_by=getattr(Chat_Logs, order_by.value),
            order=order,
            limit=limit,
            offset=offset,
            joins=[JoinExpression(model=Chat_Logs.account)],
            filters=[Accounts.id == account_id, Chat_Logs.session_id == session_id],
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
