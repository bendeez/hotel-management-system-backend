import asyncio
from tests.utils import RequestMethod
from app.config import settings
from tools.application.rate_limiter import limiter


async def test_rate_limiter(http_request, business):
    limiter._storage.storage.clear()  # provides consistent assertion
    tokens, _ = business
    tasks = []
    num_of_requests = 50
    for i in range(num_of_requests):
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
    assert len(too_many_requests) == (
        num_of_requests - settings.LIMIT_REQUESTS_PER_ENDPOINT
    )
