from enum import Enum
from app.session.models import Chat_Sessions


SessionAttributes = Enum(
    Chat_Sessions.__tablename__,
    {column.name: column.name for column in Chat_Sessions.__table__.columns},
)
