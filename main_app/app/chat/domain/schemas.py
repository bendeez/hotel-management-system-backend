from pydantic import BaseModel
from datetime import datetime


class ChatLogsCreate(BaseModel):
    session_id: str
    message: str


class ChatLogsOut(BaseModel):
    id: int
    session_id: str
    message: str
    date: datetime
