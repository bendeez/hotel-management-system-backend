import httpx
import pytest
from app.hotel_app.app import hotel_app
from tests.utils import RequestMethod, http_request, Request, Client
from typing import Optional
from datetime import datetime, timedelta
from uuid import uuid4
from app.tools.application.dependencies import get_db
from app.hotel_app.hotels.domain.models import (
    Hotels,
    Hotel_Rooms,
    Hotel_Location,
    Hotel_Review,
    Hotel_Guest_Reviews,
    Hotel_House_Rules,
)


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
def cities():
    return ["Detroit", "New York City"]


@pytest.fixture(scope="session")
async def hotels(db, cities):
    hotels = []
    for i in range(5):
        city = cities[i % 2]
        """
            not all row values have to be filled in 
        """
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
