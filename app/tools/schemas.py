from pydantic import BaseModel


class DeleteResponse(BaseModel):
    message: str
