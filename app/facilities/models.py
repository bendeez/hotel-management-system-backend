from app.tools.models.base_models import BaseMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Facility(BaseMixin):
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(10000))
