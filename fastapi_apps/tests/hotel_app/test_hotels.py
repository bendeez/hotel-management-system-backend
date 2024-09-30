from app.hotel_app.hotels.domain.models import Hotels
from tests.utils import RequestMethod
from app.hotel_app.hotels.domain.schemas import (
    HotelsOut,
    HotelRoomsOut,
    HotelGuestReviewsOut,
)
from app.hotel_app.hotels.domain.constants import HotelsAttributes
from app.tools.domain.constants import DatabaseQueryOrder


async def test_get_hotels(http_request, serialized_and_formatted_hotel_models):
    params = {
        "limit": 3,
        "offset": 0,
        "order": DatabaseQueryOrder.DESC.value,
        "order_by": HotelsAttributes.ID.value,
    }
    response = await http_request(
        path="/hotels", method=RequestMethod.GET, params=params
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == params["limit"]
    serialized_hotel_data = [HotelsOut(**d) for d in data]
    assert (
        serialized_hotel_data
        == serialized_and_formatted_hotel_models[: params["limit"]]
    )


async def test_get_hotels_by_city(
    http_request, cities, serialized_and_formatted_hotel_models
):
    params = {
        "limit": 2,
        "offset": 0,
        "order": DatabaseQueryOrder.DESC.value,
        "order_by": HotelsAttributes.ID.value,
        "city": cities[-1],
    }
    response = await http_request(
        path="/hotels", method=RequestMethod.GET, params=params
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == params["limit"]
    serialized_hotel_data = [HotelsOut(**d) for d in data]
    assert (
        serialized_hotel_data
        == list(
            filter(
                lambda h: h.hotel_location.city
                == params["city"],  # filter by param city
                serialized_and_formatted_hotel_models,
            )
        )[: params["limit"]]
    )


async def test_get_hotels_by_rating(
    http_request, serialized_and_formatted_hotel_models
):
    params = {
        "limit": 2,
        "offset": 0,
        "order": DatabaseQueryOrder.DESC.value,
        "order_by": HotelsAttributes.ID.value,
        "rating_lt": 6,
        "rating_gt": 3,
    }
    response = await http_request(
        path="/hotels", method=RequestMethod.GET, params=params
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == params["limit"]
    serialized_hotel_data = [HotelsOut(**d) for d in data]
    assert (
        serialized_hotel_data
        == list(
            filter(
                lambda h: params["rating_gt"]
                <= h.hotel_review.rating_out_of_10
                <= params["rating_lt"],  # filter by ratings
                serialized_and_formatted_hotel_models,
            )
        )[: params["limit"]]
    )
