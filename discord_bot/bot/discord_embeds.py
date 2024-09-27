from bot.hotel_embeds import HotelEmbedCreator
from dataclasses import asdict
import discord


class DiscordEmbeds:
    def __init__(self, message: discord.message):
        self.message = message

    def create_hotel_embeds(self, hotel):
        hotel_embed_creator = HotelEmbedCreator(hotel=hotel)
        hotel_embeds = hotel_embed_creator.create_hotel_embeds()
        return list(asdict(hotel_embeds).values())

    async def _send_embeds(self, embeds: list[discord.Embed]):
        for embed in embeds:
            if isinstance(embed, list):
                for e in embed:
                    await self.message.channel.send(embed=e)
            else:
                await self.message.channel.send(embed=embed)

    async def send_hotel_embeds(self, hotels):
        for hotel in hotels:
            embeds = self.create_hotel_embeds(hotel=hotel)
            await self._send_embeds(embeds=embeds)
