from app.tools.models.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text


class Business(BaseMixin):
    email: Mapped[str] = mapped_column(String(45),unique=True)
    name: Mapped[str] = String(45)
    subscription_id: Mapped[int] = mapped_column(default=1) # for development purposes
    location: Mapped[str] = String(45)
    account_type: Mapped[str] = mapped_column(ForeignKey("accounts.account_type"))


class Business_Data(BaseMixin):
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("data_categories.id"))
    data: Mapped[str] = mapped_column(Text)
    keywords: Mapped[str] = mapped_column(String(45))

class Data_Categories(BaseMixin):
    name: Mapped[str] = mapped_column(String(45))
    keywords: Mapped[str] = mapped_column(String(45))
