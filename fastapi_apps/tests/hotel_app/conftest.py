import httpx
import pytest
from app.hotel_app.app import hotel_app
from tests.utils import RequestMethod, http_request, Request, Client

from typing import Optional, Union
from datetime import datetime, timedelta
from app.hotel_app.hotels.domain.schemas import (
    HotelsOut,
    HotelRoomsOut,
    HotelGuestReviewsOut,
)
from uuid import uuid4
from tools.application.dependencies import get_db
from app.hotel_app.hotels.domain.models import (
    Hotels,
    Hotel_Rooms,
    Hotel_Location,
    Hotel_Review,
    Hotel_Guest_Reviews,
    Hotel_House_Rules,
)
import re
from sqlalchemy import inspect


@pytest.fixture(autouse=True)
async def override_dependencies(db):
    def get_test_db():
        return db

    hotel_app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="session")
def user_request():
    return Request(
        client=Client(host="127.0.0.1"), headers={"User-Agent": "Mozilla/5.0"}
    )


@pytest.fixture(scope="session")
def cities() -> list:
    return ["Detroit", "New York City"]


def camel_to_snake(camel_str):
    snake_case = re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()
    first_digit = re.search(r"\d", snake_case)
    if first_digit:
        index = first_digit.start()
        snake_case_with_digit = snake_case[:index] + "_" + snake_case[index:]
        return snake_case_with_digit
    else:
        return snake_case


def convert_camel_keys_to_snake_case(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = camel_to_snake(key)
            new_dict[new_key] = convert_camel_keys_to_snake_case(value)
        return new_dict
    elif isinstance(data, list):
        return [convert_camel_keys_to_snake_case(item) for item in data]
    else:
        return data


@pytest.fixture()
def transformed_hotels_pydantic_response() -> list[HotelsOut]:
    def _transformed_hotel_pydantic_response(hotel_data: dict):
        hotel_data_with_snake_str_keys = convert_camel_keys_to_snake_case(
            data=hotel_data
        )
        return [HotelsOut(**d) for d in hotel_data_with_snake_str_keys]

    return _transformed_hotel_pydantic_response


@pytest.fixture()
def serialize_hotel_model_value() -> Union[dict, str, None]:
    def _serialize_hotel_model_value(key, value):
        hotel_relationships = inspect(Hotels).relationships
        if key in hotel_relationships and isinstance(value, list):
            return [v.__dict__ for v in value]
        elif key in hotel_relationships and value is not None:
            return value.__dict__
        else:
            return value

    return _serialize_hotel_model_value


@pytest.fixture()
def transformed_and_formatted_hotel_database_models(
    serialize_hotel_model_value, hotels
) -> list[HotelsOut]:
    return list(
        sorted(
            [
                HotelsOut(
                    **{
                        key: serialize_hotel_model_value(key, value)
                        for key, value in hotel.__dict__.items()
                    }
                )
                for hotel in hotels
            ],
            key=lambda h: h.id,
            reverse=True,  # order by id descending
        )
    )


@pytest.fixture(scope="session")
async def hotels(db, cities) -> list[Hotels]:
    hotels = []
    for i in range(5):
        city = cities[i % 2]
        hotel = Hotels(
            title=str(uuid4()),
            description=str(uuid4()),
            amenities=[str(uuid4()), str(uuid4())],
            image_link=str(uuid4()),
            hotel_rooms=[
                Hotel_Rooms(
                    room_type=[str(uuid4())],
                    price=[str(uuid4())],
                    guest_count=[str(uuid4())],
                    guest_count_numeric=1,
                    price_numeric=100.0,
                    tax_and_fee_numeric=15.0,
                )
            ],
            hotel_review=Hotel_Review(
                rating_out_of_10=(i * 2), num_of_reviews=(i * 20)
            ),
            hotel_house_rules=Hotel_House_Rules(
                check_in=str(uuid4()), check_out=str(uuid4())
            ),
            hotel_location=Hotel_Location(city=city),
            hotel_guest_reviews=[
                Hotel_Guest_Reviews(
                    date=str(uuid4()),
                    title=str(uuid4()),
                    positive=str(uuid4()),
                    negative=str(uuid4()),
                )
                for _ in range(2)
            ],
        )
        db.add(hotel)
        hotels.append(hotel)
    await db.commit()
    [
        await db.refresh(
            hotel,
            attribute_names=[
                "hotel_review",
                "hotel_location",
                "hotel_rooms",
                "hotel_guest_reviews",
            ],
        )
        for hotel in hotels
    ]
    return hotels


@pytest.fixture(scope="session", name="client", autouse=True)
async def create_http_client():
    transport = httpx.ASGITransport(app=hotel_app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://127.0.0.1:8000"
    ) as client:
        yield client


@pytest.fixture(name="http_request")
async def make_http_request(client):
    async def _make_http_request(
        path,
        client=client,
        method=RequestMethod.GET,
        json: Optional[dict] = None,
        files=None,
        token: Optional[str] = None,
        params: Optional[dict] = None,
    ):
        data = await http_request(
            client=client,
            path=path,
            method=method,
            json=json,
            files=files,
            token=token,
            params=params,
        )
        return data

    return _make_http_request


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
