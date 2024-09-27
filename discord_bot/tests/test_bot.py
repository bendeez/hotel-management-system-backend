from uuid import uuid4


async def test_show_hotels_command(
    hotel_suggestion_bot,
    create_message,
    embeds_sent,
    separate_embeds_by_hotels_and_format,
):
    message = create_message(author=str(uuid4()), content="/show hotels")
    """
        appends embed to the embeds_sent list when the bot sends each embed
    """
    await hotel_suggestion_bot.on_message(message=message)
    print(separate_embeds_by_hotels_and_format(embeds_sent=embeds_sent))
