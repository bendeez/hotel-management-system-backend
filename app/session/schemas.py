from pydantic import BaseModel
from datetime import datetime


class SessionsOut(BaseModel):
    session_id: str
    expiry: datetime
