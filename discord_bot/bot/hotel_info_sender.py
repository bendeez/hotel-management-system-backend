import discord

class HotelInfoSender:
    def __init__(self, message, hotel):
        self.message = message
        self.hotel_title = hotel["title"]
        self.hotel = hotel

    def add_to_embed_with_dict(self, embed: discord.Embed, hotel_data: dict, filters: list):
        filters = filters or []
        for field, description in hotel_data.items():
            if field not in filters:
                field = field.replace("_", " ").replace("numeric", "")
                embed.add_field(name=field, value=description, inline=False)

    async def send_main_hotel_info(self) -> discord.Embed:
        main_hotel_info_embed = discord.Embed(colour=discord.Colour.dark_teal(), description=self.hotel["description"],
                                              title=self.hotel_title)
        main_hotel_info_embed.set_image(url=self.hotel["image_link"])
        self.add_to_embed_with_dict(embed=main_hotel_info_embed, hotel_data=self.hotel["hotel_location"],
                                    filters=["id", "hotel_id"])
        await self.message.channel.send(embed=main_hotel_info_embed)
        return main_hotel_info_embed

    async def send_hotel_review(self) -> discord.Embed:
        hotel_review_embed = discord.Embed(colour=discord.Colour.dark_teal(),
                                           title=f"{self.hotel_title} - overall review")
        self.add_to_embed_with_dict(embed=hotel_review_embed, hotel_data=self.hotel["hotel_review"],
                                    filters=["id", "hotel_id"])
        await self.message.channel.send(embed=hotel_review_embed)
        return hotel_review_embed

    async def send_hotel_amenities(self) -> discord.Embed:
        hotel_amenities = ", ".join(self.hotel["amenities"])
        amenities_embed = discord.Embed(colour=discord.Colour.dark_teal(), description=hotel_amenities,
                                        title=f"{self.hotel_title} - Amenities")
        await self.message.channel.send(embed=amenities_embed)
        return amenities_embed

    async def send_hotel_house_rules(self) -> discord.Embed:
        house_rules_embed = discord.Embed(colour=discord.Colour.dark_teal(),
                                          title=f"{self.hotel_title} - House Rules")
        self.add_to_embed_with_dict(embed=house_rules_embed, hotel_data=self.hotel["hotel_house_rules"],
                                    filters=["id", "hotel_id"])
        await self.message.channel.send(embed=house_rules_embed)
        return house_rules_embed

    async def send_all_hotel_room_info(self) -> list[discord.Embed]:
        hotel_room_embeds = []
        for room_number, room in enumerate(self.hotel["hotel_rooms"]):
            hotel_room_embed = await self.send_hotel_room_info(room_number=room_number, room=room)
            hotel_room_embeds.append(hotel_room_embed)
        return hotel_room_embeds

    async def send_hotel_room_info(self, room, room_number) -> discord.Embed:
        hotel_room_description = " - ".join(room["room_type"])
        hotel_room_embed = discord.Embed(colour=discord.Colour.dark_teal(),
                              title=f"{self.hotel_title} - Room {room_number + 1}", description=hotel_room_description)
        self.add_to_embed_with_dict(embed=hotel_room_embed, hotel_data=room,
                                    filters=["id", "hotel_id", "guest_count", "price", "room_type"])
        await self.message.channel.send(embed=hotel_room_embed)
        return {}

    async def send_all_hotel_guest_reviews(self) -> list[discord.Embed]:
        guest_review_embeds = []
        for review_number, review in enumerate(self.hotel["hotel_guest_reviews"]):
            guest_review_embed = await self.send_hotel_guest_review(review_number=review_number, review=review)
            guest_review_embeds.append(guest_review_embed)
        return guest_review_embeds

    async def send_hotel_guest_review(self, review, review_number) -> discord.Embed:
        guest_review_embed = discord.Embed(colour=discord.Colour.dark_teal(),
                              title=f"{self.hotel_title} - Guest Review {review_number + 1}")
        self.add_to_embed_with_dict(embed=guest_review_embed, hotel_data=review,
                                    filters=["id", "hotel_id"])
        await self.message.channel.send(embed=guest_review_embed)
        return guest_review_embed