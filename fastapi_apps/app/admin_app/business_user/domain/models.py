from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from app.admin_app.accounts.domain.models import Accounts


class Business_Users(Accounts):
    id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(500))
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business.id", ondelete="CASCADE")
    )
    role_name: Mapped[str] = mapped_column(String(45))

    __mapper_args__ = {"polymorphic_identity": "business_users"}
