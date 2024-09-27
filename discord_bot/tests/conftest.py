from unittest.mock import AsyncMock
import pytest
from bot.client import HotelSuggestionBot
from bot.discord_embeds import DiscordEmbeds
from tests.utils import fetch_hotel_data
import re


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
def separate_embeds_by_hotels_and_format(hotel_data):
    def find_starting_index_of_categorical_embeds(hotel_embeds, match):
        for index, h in enumerate(hotel_embeds):
            if re.search(match, h.title):
                return index

    def insert_categorical_embeds(hotel_embeds, match):
        """
        hotel embeds couldve already had an inserted categorical list inside of it
        """
        hotel_categorical_embeds = [
            h for h in hotel_embeds if isinstance(h, str) and re.search(match, h.title)
        ]
        for h in hotel_categorical_embeds:
            hotel_embeds.remove(h)
        hotel_embeds[-1] = hotel_categorical_embeds

    def _separate_embeds_by_hotels_and_format(embeds_sent):
        hotel_starting_points = [
            index
            for index, e in enumerate(embeds_sent)
            if e.title in [hotel["title"] for hotel in hotel_data]
        ]
        embeds_separated_by_hotels = []
        for i, starting_point in enumerate(hotel_starting_points):
            if (i + 1) == len(hotel_starting_points):
                """
                    makes sure that it doesnt access an index
                    outside of the starting point list range
                """
                next_hotel_reference = None
            else:
                next_hotel_reference = hotel_starting_points[i + 1]
            hotel_embeds = embeds_sent[starting_point:next_hotel_reference]
            room_match = "Room"
            guest_review_match = "Guest Review Match"
            room_starting_index = find_starting_index_of_categorical_embeds(
                hotel_embeds=hotel_embeds, match=room_match
            )
            guest_review_starting_index = find_starting_index_of_categorical_embeds(
                hotel_embeds=hotel_embeds, match=guest_review_match
            )
            assert guest_review_starting_index > room_starting_index
            insert_categorical_embeds(hotel_embeds=hotel_embeds, match=room_match)
            insert_categorical_embeds(
                hotel_embeds=hotel_embeds, match=guest_review_match
            )
            embeds_separated_by_hotels.append(hotel_embeds)
        return embeds_separated_by_hotels

    return _separate_embeds_by_hotels_and_format


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
