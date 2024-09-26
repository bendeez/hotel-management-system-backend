import httpx
import discord
from bot.config import settings
from bot.hotel_embeds import HotelEmbedCreator, HotelEmbeds


class HotelSuggestionBot:
    def __init__(self, client: discord.Client, token: str, server: str):
        self.client = client
        self.token = token
        self.server = server

    async def fetch_hotel_data(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.server}/hotels")
            hotel_data = response.json()
            return hotel_data

    async def on_ready(self):
        print(f"We have logged in as {self.client.user}")

    def create_all_hotels_embeds(self, hotels):
        hotel_embeds = []
        for hotel in hotels:
            hotel_embed = self.create_hotel_embeds(hotel=hotel)
            hotel_embeds.append(hotel_embed)

        return hotel_embeds

    async def send_hotel_embeds(self, hotel_embeds):
        pass

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith("/show hotels"):
            hotels = await self.fetch_hotel_data()
            hotel_embeds = self.create_all_hotels_embeds(hotels)

    def run(self):
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.run(self.token)


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    hotel_suggestion_bot = HotelSuggestionBot(
        client=client, token=settings.TOKEN, server="http://127.0.0.1:8000"
    )
    hotel_suggestion_bot.run()
