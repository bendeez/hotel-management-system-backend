from uuid import uuid4

async def test_show_hotels_command(hotel_suggestion_bot, create_message):
    message = create_message(author=str(uuid4()), content="/show hotels")
    await hotel_suggestion_bot.on_message(message=message)