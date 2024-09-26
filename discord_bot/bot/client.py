import httpx
import discord
from bot.config import settings
from bot.hotel_embeds import HotelEmbedCreator
from dataclasses import asdict


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

    async def send_hotel_embeds(self, hotels, message):
        for hotel in hotels[:1]:
            hotel_embed_creator = HotelEmbedCreator(hotel=hotel)
            hotel_embeds = hotel_embed_creator.create_hotel_embeds()
            for embed in list(asdict(hotel_embeds).values()):
                if isinstance(embed, list):
                    for e in embed:
                        await message.channel.send(embed=e)
                else:
                    await message.channel.send(embed=embed)

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith("/show hotels"):
            hotels = await self.fetch_hotel_data()
            await self.send_hotel_embeds(hotels=hotels, message=message)

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
