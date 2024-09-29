from pydantic import BaseModel
from datetime import datetime


class SessionsOut(BaseModel):
    id: str
    end_time: datetime
    ip_address: str
    user_agent: str
    account_id: int
