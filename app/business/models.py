from app.tools.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text
from app.accounts.models import Accounts


class Business(Accounts):
    id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    email: Mapped[str] = mapped_column(String(45), unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    name: Mapped[str] = String(45)
    subscription_id: Mapped[int] = mapped_column(default=1)  # for development purposes
    location: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(500))

    __mapper_args__ = {
        "polymorphic_identity": "business",
    }


class Business_Data(BaseMixin):
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("data_categories.id"))
    data: Mapped[str] = mapped_column(Text)
    keywords: Mapped[str] = mapped_column(String(45))


class Data_Categories(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))
    keywords: Mapped[str] = mapped_column(String(45))


class Business_Users(Accounts):
    id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    email: Mapped[str] = mapped_column(String(45), unique=True)
    password: Mapped[str] = mapped_column(String(500))
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    role_name: Mapped[str] = mapped_column(String(45))

    __mapper_args__ = {"polymorphic_identity": "business_users"}
