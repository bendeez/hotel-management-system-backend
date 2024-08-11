import httpx
from enum import Enum
from pydantic import BaseModel, EmailStr

http_server = "http://127.0.0.1:8000"


class UserMock(BaseModel):
    id: int
    email: EmailStr
    password: str
    role: str


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


async def http_request(
    client: httpx.AsyncClient,
    path,
    method=RequestMethod.GET,
    json=None,
    files=None,
    token=None,
):
    headers = {"Authorization": f"bearer {token}"}
    if method == RequestMethod.POST:
        response = await client.post(url=path, json=json, data=files, headers=headers)
    elif method == RequestMethod.PUT:
        response = await client.put(url=path, json=json, data=files, headers=headers)
    elif method == RequestMethod.GET:
        response = await client.get(url=path, headers=headers)
    elif method == RequestMethod.DELETE:
        response = await client.request(
            url=path, method="DELETE", json=json, headers=headers
        )
    else:
        raise ValueError("Invalid method")
    return response
