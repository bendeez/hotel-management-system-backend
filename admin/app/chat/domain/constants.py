from enum import Enum
from app.chat.domain.models import Chat_Logs


ChatsAttributes = Enum(
    Chat_Logs.__tablename__,
    {column.name: column.name for column in Chat_Logs.__table__.columns},
)
