from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.admin_app.accounts.domain.models import Accounts


class Users(Accounts):
    id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(100), unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column(String(500))

    __mapper_args__ = {"polymorphic_identity": "users"}
