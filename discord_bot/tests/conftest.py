from unittest.mock import AsyncMock
import pytest
from bot.client import HotelSuggestionBot
from tests.utils import fetch_hotel_data

@pytest.fixture()
def bot_client_username():
    return "bot"

@pytest.fixture()
def bot_client(bot_client_username):
    client = AsyncMock()
    client.user = bot_client_username
    return client

@pytest.fixture()
def hotel_suggestion_bot(bot_client):
    bot = HotelSuggestionBot(client=bot_client, token="token", server="http://mock:8000")
    bot.fetch_hotel_data = fetch_hotel_data
    return bot

@pytest.fixture()
def create_message():
    def _create_message(author: str, content: str):
        message = AsyncMock()
        message.author = author
        message.content = content
        return message
    return _create_message


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
