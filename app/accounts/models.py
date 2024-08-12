from app.tools.models.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class Accounts(BaseMixin):
    type: Mapped[str] = mapped_column(String(45))

    __mapper_args__ = {
        "polymorphic_identity": "accounts",
        "polymorphic_on": "type",
    }


class Business_Users(Accounts):
    id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    username: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(500))
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    __mapper_args__ = {"polymorphic_identity": "business_users"}


class Roles(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))


class Role_Permissions(BaseMixin):
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))


class Permissions(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))
    slug_value: Mapped[str] = mapped_column(String(45))
