from app.tools.models.base_models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String
from datetime import datetime
from typing import Optional


class Chats(Base):
    __tablename__ = "chats"
    message_id: Mapped[str] = mapped_column(String(45), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(45))
    chat_id: Mapped[str] = mapped_column(String(45))
    message: Mapped[str] = mapped_column(Text)
    messenger: Mapped[str] = mapped_column(String(45))
    message_time: Mapped[datetime] = mapped_column(default=datetime.now())
    environment: Mapped[Optional[str]] = mapped_column(String(45))


class Sessions(Base):
    __tablename__ = "sessions"
    session_id: Mapped[str] = mapped_column(String(45), primary_key=True)
    expiry: Mapped[datetime]
