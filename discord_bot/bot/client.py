import httpx
import discord
from bot.config import settings
from bot.hotel_info_sender import HotelInfoSender

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
        print(f'We have logged in as {self.client.user}')

    async def send_hotel(self, message, hotel):
        hotel_info_sender = HotelInfoSender(message=message, hotel=hotel)
        hotel_main_info = await hotel_info_sender.send_main_hotel_info()
        hotel_review = await hotel_info_sender.send_hotel_review()
        hotel_amenities = await hotel_info_sender.send_hotel_amenities()
        hotel_house_rules = await hotel_info_sender.send_hotel_house_rules()
        hotel_room_info = await hotel_info_sender.send_all_hotel_room_info()
        hotel_guest_reviews = await hotel_info_sender.send_all_hotel_guest_reviews()

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith('/show hotels'):
            hotels = await self.fetch_hotel_data()
            for hotel in hotels[:1]:
                await self.send_hotel(hotel=hotel, message=message)

    def run(self):
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.run(self.token)

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    hotel_suggestion_bot = HotelSuggestionBot(client=client, token=settings.TOKEN, server="http://127.0.0.1:8000")
    hotel_suggestion_bot.run()


