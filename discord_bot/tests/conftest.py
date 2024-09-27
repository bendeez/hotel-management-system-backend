from unittest.mock import AsyncMock
import pytest
from bot.client import HotelSuggestionBot
from bot.discord_embeds import DiscordEmbeds
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
async def hotel_data():
    data = await fetch_hotel_data()
    return data


@pytest.fixture()
def hotel_suggestion_bot(bot_client):
    bot = HotelSuggestionBot(
        client=bot_client, token="token", server="http://mock:8000"
    )
    bot.fetch_hotel_data = fetch_hotel_data
    return bot


@pytest.fixture()
def find_embeds_per_dict():
    def _find_embeds_per_dict(hotel_data: list, discord_embeds: DiscordEmbeds):
        embeds_per_dict = []
        for hotel in hotel_data:
            embeds = discord_embeds.create_hotel_embeds(hotel=hotel)
            for embed in embeds:
                if isinstance(embed, list):
                    for e in embed:
                        embeds_per_dict.append(e)
                else:
                    embeds_per_dict.append(embed)
        return embeds_per_dict

    return _find_embeds_per_dict


@pytest.fixture()
def sort_embeds_by_title():
    def _sort_embeds_by_title(embeds_list: list):
        return list(sorted(embeds_list, key=lambda e: e.title))

    return _sort_embeds_by_title


@pytest.fixture()
def embeds_sent():
    return []


@pytest.fixture()
def create_message(embeds_sent):
    def _create_message(author: str, content: str):
        async def send_message(embed):
            embeds_sent.append(embed)

        message = AsyncMock()
        message.author = author
        message.content = content
        message.channel.send = send_message
        return message

    return _create_message


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
