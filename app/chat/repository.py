from app.facility.repository import BaseRepository
from app.chat.constants import ChatsAttributes
from app.tools.constants import DatabaseQueryOrder
from app.chat.models import Chat_Messages


class ChatRepository(BaseRepository):
    async def get_all_chat_logs(
        self,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_logs = await self.get_all(
            model=Chat_Messages,
            order_by=getattr(Chat_Messages, order_by.value),
            order=order,
            offset=offset,
            limit=limit,
        )
        return chat_logs

    async def get_chat_logs_by_session_id(
        self,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_logs = await self.get_all(
            model=Chat_Messages,
            order_by=getattr(Chat_Messages, order_by.value),
            order=order,
            limit=limit,
            offset=offset,
            filter={Chat_Messages.session_id: session_id},
        )
        return chat_logs
