from pydantic import BaseModel
from datetime import datetime


class SessionsOut(BaseModel):
    id: str
    expiry: datetime
    ip_address: str
    user_agent: str
