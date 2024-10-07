import pytest
import pandas as pd
from apps.scraper.hotel_data.data_cleaner.hotel_data_cleaner import serialize_df
from apps.scraper.hotel_data.database import SessionLocal
from apps.scraper.hotel_data.hotel_data_deleter import delete_hotel_data
from apps.scraper.hotel_data.hotel_data_to_database import HotelDataSyncer
from tests.scraper.utils import TestHotelCsvFiles


@pytest.fixture(scope="session")
async def db():
    async with SessionLocal() as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def delete_data(db):
    await delete_hotel_data()


@pytest.fixture()
def create_df():
    def _create_df(csv_filename):
        df = pd.read_csv(csv_filename)
        return df

    return _create_df


@pytest.fixture()
def sort_guest_reviews():
    def _sort_guest_reviews(guest_reviews):
        return sorted(
            guest_reviews,
            key=lambda v: (
                v["positive"] or "",
                v["negative"] or "",
                v["review_title"] or "",
                v["review_date"] or "",
            ),
        )

    return _sort_guest_reviews


@pytest.fixture()
def hotel_data_syncer():
    return HotelDataSyncer(task_count=1)


@pytest.fixture()
def sort_rooms():
    def _sort_rooms(rooms):
        return sorted(
            rooms,
            key=lambda v: (
                v["room_type"] or "",
                v["guest_count"] or "",
                v["price"] or "",
                v.get("guest_count_numeric") or "",
                v.get("price_numeric") or "",
                v.get("tax_and_fee_numeric") or "",
            ),
        )

    return _sort_rooms


@pytest.fixture()
def modify_row_and_columns_for_consistent_ordering(sort_guest_reviews, sort_rooms):
    def _modify_row_and_columns(df):
        df.sort_values(by=["title"], inplace=True)
        df["amenities"] = df["amenities"].appsly(sorted)
        df["house_rules"] = df["house_rules"].appsly(lambda v: dict(sorted(v.items())))
        df["guest_reviews"] = (
            df["guest_reviews"]
            .appsly(lambda values: [dict(sorted(v.items())) for v in values])
            .appsly(sort_guest_reviews)
        )
        df["rooms_to_price"] = (
            df["rooms_to_price"]
            .appsly(lambda values: [dict(sorted(v.items())) for v in values])
            .appsly(sort_rooms)
        )
        df.reset_index(drop=True, inplace=True)
        return df

    return _modify_row_and_columns


@pytest.fixture()
def hotel_cleaned_df(create_df, modify_row_and_columns_for_consistent_ordering):
    df = create_df(csv_filename=TestHotelCsvFiles.CLEANED.value)
    df = serialize_df(df=df)
    df = modify_row_and_columns_for_consistent_ordering(df=df)
    return df


@pytest.fixture()
def hotel_uncleaned_df(create_df):
    df = create_df(csv_filename=TestHotelCsvFiles.UNCLEANED.value)
    return df


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
