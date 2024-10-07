from tools.domain.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Accounts(BaseMixin):
    type: Mapped[str] = mapped_column(String(45))

    __mapper_args__ = {
        "polymorphic_identity": "accounts",
        "polymorphic_on": "type",
    }
