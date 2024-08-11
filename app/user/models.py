from app.tools.models.base_models import BaseMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Users(BaseMixin):
    email: Mapped[str] = mapped_column(String(45), unique=True)
    password: Mapped[str] = mapped_column(String(500))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    account_type: Mapped[str] = mapped_column(ForeignKey("accounts.account_type"))

class Roles(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))

class Role_Permissions(BaseMixin):
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

class Permissions(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))
    slug_value: Mapped[str] = mapped_column(String(45))
