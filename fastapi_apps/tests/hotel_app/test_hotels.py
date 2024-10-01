from app.hotel_app.hotels.domain.models import Hotels
from tests.utils import RequestMethod
from tests.hotel_app.utils import query_items
from app.hotel_app.hotels.domain.schemas import (
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


# async def test_get_hotels_by_city(
#     http_request, cities, serialized_and_formatted_hotel_models
# ):
#     params = {
#         "limit": 2,
#         "offset": 0,
#         "order": DatabaseQueryOrder.DESC.value,
#         "order_by": HotelsAttributes.ID.value,
#         "city": cities[-1],
#     }
#     response = await http_request(
#         path="/hotels", method=RequestMethod.GET, params=params
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == params["limit"]
#     serialized_hotel_data = [HotelsOut(**d) for d in data]
#     assert (
#         serialized_hotel_data
#         == list(
#             filter(
#                 lambda h: h.hotel_location.city
#                 == params["city"],  # filter by param city
#                 serialized_and_formatted_hotel_models,
#             )
#         )[: params["limit"]]
#     )


# async def test_get_hotels_by_rating(
#     http_request, serialized_and_formatted_hotel_models
# ):
#     params = {
#         "limit": 2,
#         "offset": 0,
#         "order": DatabaseQueryOrder.DESC.value,
#         "order_by": HotelsAttributes.ID.value,
#         "rating_lt": 6,
#         "rating_gt": 3,
#     }
#     response = await http_request(
#         path="/hotels", method=RequestMethod.GET, params=params
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == params["limit"]
#     serialized_hotel_data = [HotelsOut(**d) for d in data]
#     assert (
#         serialized_hotel_data
#         == list(
#             filter(
#                 lambda h: params["rating_gt"]
#                 <= h.hotel_review.rating_out_of_10
#                 <= params["rating_lt"],  # filter by ratings
#                 serialized_and_formatted_hotel_models,
#             )
#         )[: params["limit"]]
#     )
