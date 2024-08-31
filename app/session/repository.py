from app.tools.constants import DatabaseQueryOrder
from app.session.constants import SessionAttributes
from app.session.models import Chat_Sessions
from app.tools.base_repository import BaseRepository


class SessionRepository(BaseRepository):
    async def get_chat_sessions(
        self,
        order: DatabaseQueryOrder,
        order_by: SessionAttributes,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_sessions = await self._get_all(
            model=Chat_Sessions,
            limit=limit,
            offset=offset,
            order_by=getattr(Chat_Sessions, order_by.value),
            order=order,
        )
        return chat_sessions

    async def get_chat_session_by_id(self, session_id: str):
        session = await self._get_one(
            model=Chat_Sessions, filters=[Chat_Sessions.id == session_id]
        )
        return session
