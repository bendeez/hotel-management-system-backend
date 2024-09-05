from admin.app.accounts.models import Accounts
from admin.app.tools.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime
from datetime import timedelta
from admin.app.config import settings


class Chat_Sessions(BaseMixin):
    id: Mapped[str] = mapped_column(String(45), primary_key=True)
    account_id: Mapped[[int]] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE")
    )
    start_time: Mapped[datetime] = mapped_column(default=datetime.now())
    end_time: Mapped[datetime] = mapped_column(
        default=datetime.now() + timedelta(minutes=settings.SESSION_DURATION)
    )
    ip_address: Mapped[str] = mapped_column(String(45))
    user_agent: Mapped[str] = mapped_column(String(45))

    account: Mapped["Accounts"] = relationship(viewonly=True)
