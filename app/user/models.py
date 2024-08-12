from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.accounts.models import Accounts


class Users(Accounts):
    id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    email: Mapped[str] = mapped_column(String(45), unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column(String(500))

    __mapper_args__ = {"polymorphic_identity": "users"}
