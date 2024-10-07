from apps.hotel_app.hotels.domain.models import Hotels
from tests.utils import RequestMethod
from tests.hotel_app.utils import query_items
from apps.hotel_app.hotels.domain.schemas import (
    HotelsOut,
    HotelRoomsOut,
    HotelGuestReviewsOut,
)


async def test_get_hotels(
    http_request,
    transformed_and_formatted_hotel_database_models,
    transformed_hotels_pydantic_response,
):
    limit = 3
    order = "DESC"
    order_by = "ID"
    query = f"""
            query MyQuery {{
                hotels(limit: {limit}, order: {order}, orderBy: {order_by}) {{
                    {query_items}
                }}
            }}
            """
    response = await http_request(
        path="/hotels", method=RequestMethod.POST, json={"query": query}
    )
    assert response.status_code == 200
    data = response.json()["data"]["hotels"]
    assert len(data) == limit
    hotels_pydantic_response = transformed_hotels_pydantic_response(hotel_data=data)
    assert (
        hotels_pydantic_response
        == transformed_and_formatted_hotel_database_models[:limit]
    )


async def test_get_hotels_by_city(
    http_request,
    cities,
    transformed_and_formatted_hotel_database_models,
    transformed_hotels_pydantic_response,
):
    limit = 2
    order = "DESC"
    order_by = "ID"
    city = cities[-1]
    query = f"""
            query MyQuery {{
                hotels(limit: {limit}, order: {order}, orderBy: {order_by}, city: "{city}") {{
                    {query_items}
                }}
            }}
            """
    response = await http_request(
        path="/hotels", method=RequestMethod.POST, json={"query": query}
    )
    assert response.status_code == 200
    data = response.json()["data"]["hotels"]
    assert len(data) == limit
    hotels_pydantic_response = transformed_hotels_pydantic_response(hotel_data=data)
    assert (
        hotels_pydantic_response
        == list(
            filter(
                lambda h: h.hotel_location.city == city,  # filter by param city
                transformed_and_formatted_hotel_database_models,
            )
        )[:limit]
    )


async def test_get_hotels_by_rating(
    http_request,
    transformed_and_formatted_hotel_database_models,
    transformed_hotels_pydantic_response,
):
    limit = 2
    order = "DESC"
    order_by = "ID"
    rating_lt = 6
    rating_gt = 3
    query = f"""
            query MyQuery {{
                hotels(limit: {limit}, order: {order}, orderBy: {order_by}, ratingGt: {rating_gt}, ratingLt: {rating_lt}) {{
                    {query_items}
                }}
            }}
            """
    response = await http_request(
        path="/hotels", method=RequestMethod.POST, json={"query": query}
    )
    assert response.status_code == 200
    data = response.json()["data"]["hotels"]
    assert len(data) == limit
    hotels_pydantic_response = transformed_hotels_pydantic_response(hotel_data=data)
    assert (
        hotels_pydantic_response
        == list(
            filter(
                lambda h: rating_gt
                <= h.hotel_review.rating_out_of_10
                <= rating_lt,  # filter by ratings
                transformed_and_formatted_hotel_database_models,
            )
        )[:limit]
    )
