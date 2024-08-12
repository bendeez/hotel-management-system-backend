from app.tools.models.base_models import BaseMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.accounts.models import Accounts


class Users(Accounts):
    id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    email: Mapped[str] = mapped_column(String(45), unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column(String(500))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    business_id: Mapped[Optional[int]] = mapped_column(ForeignKey("business.id"))

class Roles(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))

class Role_Permissions(BaseMixin):
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

class Permissions(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))
    slug_value: Mapped[str] = mapped_column(String(45))
