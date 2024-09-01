import httpx
from enum import Enum
from dataclasses import dataclass
from typing import Optional

http_server = "http://127.0.0.1:8000"


@dataclass
class Client:
    host: str


@dataclass
class Request:
    client: Client
    headers: dict


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


async def http_request(
    client: httpx.AsyncClient,
    path,
    method=RequestMethod.GET,
    json: Optional[dict] = None,
    files=None,
    token: Optional[str] = None,
    params: Optional[dict] = None,
):
    headers = {"Authorization": f"bearer {token}"}
    if method == RequestMethod.POST:
        response = await client.post(
            url=path, json=json, data=files, headers=headers, params=params
        )
    elif method == RequestMethod.PUT:
        response = await client.put(
            url=path, json=json, data=files, headers=headers, params=params
        )
    elif method == RequestMethod.GET:
        response = await client.get(url=path, headers=headers, params=params)
    elif method == RequestMethod.DELETE:
        response = await client.request(
            url=path, method="DELETE", json=json, headers=headers, params=params
        )
    else:
        raise ValueError("Invalid method")
    return response
