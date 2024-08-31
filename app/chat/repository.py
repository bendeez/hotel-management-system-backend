from app.chat.constants import ChatsAttributes
from app.tools.constants import DatabaseQueryOrder
from app.chat.models import Chat_Messages
from app.session.repository import SessionRepository
from app.accounts.models import Accounts
from app.tools.base_repository import JoinExpression


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
            model=Chat_Messages,
            order_by=getattr(Chat_Messages, order_by.value),
            order=order,
            offset=offset,
            limit=limit,
            joins=[JoinExpression(model=Chat_Messages.account)],
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
            model=Chat_Messages,
            order_by=getattr(Chat_Messages, order_by.value),
            order=order,
            limit=limit,
            offset=offset,
            joins=[JoinExpression(model=Chat_Messages.account)],
            filters=[Accounts.id == account_id, Chat_Messages.session_id == session_id],
        )
        return chat_logs
