from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatLogsOut(BaseModel):
    message_id: str
    session_id: str
    chat_id: str
    message: str
    messenger: str
    message_time: datetime
    environment: Optional[str] = None


class SessionsOut(BaseModel):
    session_id: str
    expiry: datetime
