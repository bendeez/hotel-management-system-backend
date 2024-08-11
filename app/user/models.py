from app.tools.models.base_models import BaseMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Users(BaseMixin):
    email: Mapped[str] = mapped_column(String(45), unique=True)
    password: Mapped[str] = mapped_column(String(500))
    role: Mapped[str] = mapped_column(String(45), default="user")
