from app.tools.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class Facility(BaseMixin):
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(10000))
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
