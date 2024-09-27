from uuid import uuid4
from bot.discord_embeds import DiscordEmbeds
import re 


async def test_show_hotels_command(
    hotel_suggestion_bot,
    create_message,
    embeds_sent,
    hotel_data,
    find_embeds_per_dict,
    sort_embeds_by_title,
):
    message = create_message(author=str(uuid4()), content="/show hotels")
    """
        appends embed to the embeds_sent list when the bot sends each embed
    """
    await hotel_suggestion_bot.on_message(message=message)
    discord_embeds = DiscordEmbeds(message=message)
    hotel_data_embeds = find_embeds_per_dict(
        hotel_data=hotel_data, discord_embeds=discord_embeds
    )
    assert len(hotel_data_embeds) == len(embeds_sent)
    assert sort_embeds_by_title(hotel_data_embeds) == sort_embeds_by_title(embeds_sent)
    hotel_starting_points = [index for index, e in enumerate(embeds_sent) if e.title in [hotel["title"] for hotel in hotel_data]]
    embeds_separated_by_hotels = []
    for i, starting_point in enumerate(hotel_starting_points):
        if (i + 1) == len(hotel_starting_points):
            """
                makes sure that it doesnt access an index
                outside of the starting point list range
            """
            next_hotel_reference = None
        else:
            next_hotel_reference = hotel_starting_points[i+1]
            hotel_embdeds = embeds_sent[starting_point:next_hotel_reference]
        print([index for index, h in enumerate(hotel_embdeds) if re.search(r"Guest Review", h.title)])
        embeds_separated_by_hotels.append(embeds_sent[starting_point:next_hotel_reference])


    
