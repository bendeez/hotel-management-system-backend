from enum import Enum


class ChatsAttributes(Enum):
    message_id = "message_id"
    session_id = "session_id"
    chat_id = "chat_id"
    message = "message"
    messenger = "messenger"
    message_time = "message_time"
    environment = "environment"


class SessionAttributes(Enum):
    session_id = "session_id"
    expiry = "expiry"
