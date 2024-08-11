from app.tools.models.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.business.models import Business
from app.user.models import Users


class Accounts(BaseMixin):
    account_type: Mapped[str] = mapped_column(String(45))
    business_accounts: Mapped[list["Business"]] = relationship(back_populates="account_type")
    user_accounts: Mapped[list["Users"]] = relationship(back_populates="account_type")