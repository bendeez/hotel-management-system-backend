from pydantic import BaseModel


class TokenRequest(BaseModel):
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class TokenCreate(AccessToken):
    refresh_token: str
