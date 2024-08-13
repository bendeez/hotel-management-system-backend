from app.tools.models.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String, ForeignKey
from datetime import datetime


class Chat_Messages(BaseMixin):
    session_id: Mapped[str] = mapped_column(ForeignKey("chat_sessions.id"))
    message: Mapped[str] = mapped_column(Text)
    messenger_id: Mapped[int] = mapped_column(ForeignKey("chat_messenger.id"))
    chat_id: Mapped[int]
    date: Mapped[datetime] = mapped_column(default=datetime.now())


class Chat_Messenger(BaseMixin):
    type: Mapped[str] = mapped_column(String(45))
    __mapper_args__ = {
        "polymorphic_identity": "chat_messenger",
        "polymorphic_on": "type",
    }


class Chat_User(Chat_Messenger):
    id: Mapped[int] = mapped_column(ForeignKey("chat_messenger.id"), primary_key=True)
    ip_address: Mapped[str] = mapped_column(String(45))
    user_agent: Mapped[str] = mapped_column(String(45))

    __mapper_args__ = {
        "polymorphic_identity": "chat_user",
    }

class Chat_Agent(Chat_Messenger):
    id: Mapped[int] = mapped_column(ForeignKey("chat_messenger.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "chat_agent",
    }

class Chat_Sessions(BaseMixin):
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
