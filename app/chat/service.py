from app.chat.repository import ChatRepository
from fastapi import Depends
from app.chat.constants import ChatsAttributes
from app.tools.constants import DatabaseQueryOrder
from app.chat.schemas import ChatLogsCreate
from app.session.exceptions import SessionNotExists, SessionForbidden, SessionExpired
from app.chat.exceptions import ChatLogNotFound
from app.chat.models import Chat_Logs
from app.accounts.models import Accounts
from datetime import datetime


class ChatService:
    def __init__(self, repository: ChatRepository = Depends(ChatRepository)):
        self.repository = repository

    async def get_all_account_chat_logs(
        self,
        account: Accounts,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_logs = await self.repository.get_all_account_chat_logs(
            order_by=order_by,
            order=order,
            offset=offset,
            limit=limit,
            account_id=account.id,
        )
        return chat_logs

    async def get_chat_logs_by_session_id(
        self,
        account: Accounts,
        order: DatabaseQueryOrder,
        order_by: ChatsAttributes,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ):
        chat_logs = await self.repository.get_account_chat_logs_by_session_id(
            account_id=account.id,
            order_by=order_by,
            order=order,
            limit=limit,
            offset=offset,
            session_id=session_id,
        )
        return chat_logs

    async def create_chat_log(self, account: Accounts, chat_log: ChatLogsCreate):
        session = await self.repository.get_chat_session_by_id(
            session_id=chat_log.session_id
        )
        if session is None:
            raise SessionNotExists()
        if account.id != session.account_id:
            raise SessionForbidden()
        if datetime.now() >= session.end_time:
            raise SessionExpired()
        chat_log = await self.repository.create(
            model_instance=Chat_Logs(**chat_log.model_dump())
        )
        return chat_log

    async def delete_chat_log(self, chat_log_id: id, account: Accounts):
        chat_log = await self.repository.get_account_chat_log_by_id(
            account_id=account.id, chat_log_id=chat_log_id
        )
        if chat_log is None:
            raise ChatLogNotFound()
        await self.repository.delete(model_instance=chat_log)
