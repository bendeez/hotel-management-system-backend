from uuid import uuid4
from bot.discord_embeds import DiscordEmbeds


async def test_on_message_event_with_message_sent_by_bot(
    hotel_suggestion_bot, create_message, embeds_sent, bot_client_username
):
    message = create_message(author=bot_client_username, content="/show hotels")
    await hotel_suggestion_bot.on_message(message=message)
    """
        make sure no messages are sent by the on message event whenever a message
        is sent by a bot to avoid sending messages in an infinate loop
    """
    assert embeds_sent == []


async def test_show_hotels_command(
    hotel_suggestion_bot,
    create_message,
    embeds_sent,
    separate_embeds_by_hotels_and_format,
    hotel_data,
):
    message = create_message(author=str(uuid4()), content="/show hotels")
    """
        appends embed to the embeds_sent list when the bot sends each embed
    """
    await hotel_suggestion_bot.on_message(message=message)
    discord_embeds = DiscordEmbeds(message=message)
    hotel_data_to_embeds = [
        discord_embeds.create_hotel_embeds(hotel=hotel) for hotel in hotel_data
    ]
    hotel_embeds_sent_formated_for_comparison = separate_embeds_by_hotels_and_format(
        embeds_sent=embeds_sent
    )
    assert hotel_embeds_sent_formated_for_comparison == hotel_data_to_embeds
