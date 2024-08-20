from app.tools.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from datetime import datetime
from typing import Optional


class Chat_Sessions(BaseMixin):
    id: Mapped[str] = mapped_column(String(45), primary_key=True)
    account_id: Mapped[Optional[int]] = mapped_column(ForeignKey("accounts.id"))
    start_time: Mapped[datetime] = mapped_column(default=datetime.now())
    end_time: Mapped[Optional[datetime]]
