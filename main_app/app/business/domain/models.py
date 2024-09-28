from app.tools.domain.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text
from app.accounts.domain.models import Accounts


class Business(Accounts):
    id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(100), unique=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    name: Mapped[str] = String(100)
    subscription_id: Mapped[int] = mapped_column(default=1)  # for development purposes
    location: Mapped[str] = mapped_column(String(45))
    password: Mapped[str] = mapped_column(String(500))

    __mapper_args__ = {
        "polymorphic_identity": "domain",
    }


class Business_Data(BaseMixin):
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business.id", ondelete="CASCADE")
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("data_categories.id", ondelete="CASCADE")
    )
    data: Mapped[str] = mapped_column(Text)
    keywords: Mapped[str] = mapped_column(String(45))


class Data_Categories(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))
    keywords: Mapped[str] = mapped_column(String(45))
