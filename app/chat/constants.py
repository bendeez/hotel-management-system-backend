from enum import Enum
from app.chat.models import Chat_Messages




ChatsAttributes = Enum(Chat_Messages.__tablename__,[column.name for column in Chat_Messages.__table__.columns])

