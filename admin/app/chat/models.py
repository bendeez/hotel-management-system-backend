from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from datetime import datetime
from admin.app.tools.base_models import BaseMixin


class Chat_Logs(BaseMixin):
    session_id: Mapped[str] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE")
    )
    message: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(default=datetime.now())

    account: Mapped["Accounts"] = relationship(secondary="chat_sessions", viewonly=True)
