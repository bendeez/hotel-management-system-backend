from app.hotels.domain.models import Hotels
from tests.utils import RequestMethod
from app.hotels.domain.schemas import HotelsOut, HotelRoomsOut, HotelGuestReviewsOut
from sqlalchemy import inspect
from app.hotels.domain.constants import HotelsAttributes
from app.tools.domain.constants import DatabaseQueryOrder


async def test_get_hotels(http_request, hotels):
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
    hotel_relationships = inspect(Hotels).relationships

    def serialize_value(key, value):
        if key in hotel_relationships and isinstance(value, list):
            return [v.__dict__ for v in value]
        elif key in hotel_relationships and value is not None:
            return value.__dict__
        else:
            return value

    assert (
        [HotelsOut(**d) for d in data]
        == list(
            sorted(
                [
                    HotelsOut(
                        **{
                            key: serialize_value(key, value)
                            for key, value in hotel.__dict__.items()
                        }
                    )
                    for hotel in hotels
                ],
                key=lambda h: h.id,
                reverse=True,  # order by id descending
            )
        )[: params["limit"]]
    )


async def test_get_hotels_by_city(http_request, hotels, cities):
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
    hotel_relationships = inspect(Hotels).relationships

    def serialize_value(key, value):
        if key in hotel_relationships and isinstance(value, list):
            return [v.__dict__ for v in value]
        elif key in hotel_relationships and value is not None:
            return value.__dict__
        else:
            return value

    """
        HotelsOut serializes the json returned by the response
        and the sqlalchemy models so they can be compared 
        (also the response model)
    """
    assert (
        [HotelsOut(**d) for d in data]
        == list(
            sorted(
                filter(
                    lambda h: h.hotel_location.city
                    == params["city"],  # filter by param city
                    [
                        HotelsOut(
                            **{
                                key: serialize_value(key, value)
                                for key, value in hotel.__dict__.items()
                            }
                        )
                        for hotel in hotels
                    ],
                ),
                key=lambda h: h.id,
                reverse=True,  # order by id descending
            )
        )[: params["limit"]]
    )
