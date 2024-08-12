from enum import Enum


class ChatsAttributes(Enum):
    message_id = "message_id"
    session_id = "session_id"
    chat_id = "chat_id"
    message = "message"
    messenger = "messenger"
    date = "date"
    environment = "environment"


class SessionAttributes(Enum):
    session_id = "session_id"
    start_time = "start_time"
    end_time = "end_time"
