import asyncio
from utils import RequestMethod
from app.config import settings


async def test_rate_limiter(http_request, business):
    tokens, _ = business
    tasks = []
    for i in range(20):
        tasks.append(
            asyncio.create_task(
                http_request(
                    path="/business/me",
                    method=RequestMethod.GET,
                    token=tokens.access_token,
                )
            )
        )
    responses = await asyncio.gather(*tasks)
    too_many_requests = list(
        filter(lambda response: response.status_code == 429, responses)
    )
    assert len(too_many_requests) == (20 - settings.LIMIT_REQUESTS_PER_ENDPOINT)
