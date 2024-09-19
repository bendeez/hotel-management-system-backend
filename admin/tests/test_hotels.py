from app.hotels.domain.models import Hotels
from tests.utils import RequestMethod
from app.hotels.domain.schemas import HotelsOut, HotelRoomsOut, HotelGuestReviewsOut
from sqlalchemy import inspect


async def test_get_all_hotels(http_request, hotels):
    response = await http_request(path="/hotels", method=RequestMethod.GET)
    assert response.status_code == 200
    data = response.json()
    hotel_relationships = inspect(Hotels).relationships

    def serialize_value(key, value):
        if key in hotel_relationships and isinstance(value, list):
            return [v.__dict__ for v in value]
        elif key in hotel_relationships and value is not None:
            return value.__dict__
        else:
            return value

    assert sorted([HotelsOut(**d) for d in data], key=lambda h: h.id) == sorted(
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
    )
