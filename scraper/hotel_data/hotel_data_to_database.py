import asyncio
from hotel_data.database import SessionLocal
from hotel_data.models import (
    Hotels,
    Hotel_Rooms,
    Hotel_Location,
    Hotel_Review,
    Hotel_Guest_Reviews,
    Hotel_House_Rules,
)
import numpy as np
from sqlalchemy import insert, select, func
from typing import Any

"""
    SET GLOBAL FOREIGN_KEY_CHECKS=0
    to get rid of parent table locks
    and overhead 
"""
async def get_max_hotel_id():
    async with SessionLocal() as db:
        max_hotel_id = await db.execute(func.max(Hotels.id))
        return max_hotel_id.scalar()


async def insert_partitioned_entities(entities: list[dict], model: Any):
    async with SessionLocal() as db:
        await db.execute(insert(model), entities)
        await db.commit()


async def insert_entities_into_database(
    task_count: int, entities: list[dict], model: Any
):
    tasks = []
    hotel_chunk = len(entities) / task_count
    for i in range(task_count):
        partitioned_entities = entities[
            int(i * hotel_chunk) : int((i + 1) * hotel_chunk)
        ]
        tasks.append(
            insert_partitioned_entities(entities=partitioned_entities, model=model)
        )
    await asyncio.gather(*tasks)


async def insert_hotels_into_database(df):
    hotels = []
    for index, hotel in df.iterrows():
        hotel = {
            "title": hotel["title"],
            "image_link": hotel["image_link"],
            "description": hotel["description"],
            "amenities": hotel["amenities"],
        }
        hotels.append(hotel)
    await insert_entities_into_database(task_count=3, entities=hotels, model=Hotels)


async def sync_hotel_data_to_database(df):
    df = df.replace({np.nan: None}).sort_values(by=["title"])
    max_hotel_id = await get_max_hotel_id()
    await insert_hotels_into_database(df)
    async with SessionLocal() as db:
        id_filter = True
        if max_hotel_id:
            id_filter = Hotels.id > max_hotel_id
        hotel_ids = await db.execute(
            select(Hotels.id).where(id_filter).order_by(Hotels.title)
        )
        hotel_ids = hotel_ids.scalars().all()
        df["id"] = hotel_ids
        bulk_inserts_by_table = {
            Hotel_Rooms: [],
            Hotel_Location: [],
            Hotel_Review: [],
            Hotel_Guest_Reviews: [],
            Hotel_House_Rules: [],
        }
        for index, hotel in df.iterrows():
            rooms_to_price = hotel["rooms_to_price"]
            hotel_rooms = (
                [
                    {
                        "room_type": room.get("room_type"),
                        "price": room.get("price"),
                        "guest_count": room.get("guest_count"),
                        "guest_count_numeric": room.get("guest_count_numeric"),
                        "price_numeric": room.get("price_numeric"),
                        "tax_and_fee_numeric": room.get("tax_and_fee_numeric"),
                        "hotel_id": hotel["id"],
                    }
                    for room in rooms_to_price
                    if isinstance(room, dict)
                ]
                if isinstance(rooms_to_price, list)
                else []
            )
            bulk_inserts_by_table[Hotel_Rooms].extend(hotel_rooms)
            hotel_review = {
                "subjective_rating": hotel["subjective_rating"],
                "num_of_reviews": hotel["num_of_reviews"],
                "staff_rating_out_of_10": hotel["staff_rating_out_of_10"],
                "facilities_rating_out_of_10": hotel["facilities_rating_out_of_10"],
                "cleanliness_rating_out_of_10": hotel["cleanliness_rating_out_of_10"],
                "comfort_rating_out_of_10": hotel["comfort_rating_out_of_10"],
                "value_for_money_rating_out_of_10": hotel[
                    "value_for_money_rating_out_of_10"
                ],
                "rating_out_of_10": hotel["rating_out_of_10"],
                "location_rating_out_of_10": hotel["location_rating_out_of_10"],
                "free_wifi_rating_out_of_10": hotel["free_wifi_rating_out_of_10"],
                "hotel_id": hotel["id"],
            }
            bulk_inserts_by_table[Hotel_Review].append(hotel_review)
            house_rules = hotel["house_rules"]
            hotel_house_rules = (
                {
                    "check_in": house_rules.get("Check-in"),
                    "check_out": house_rules.get("Check-out"),
                    "cancellation_payment": house_rules.get("Cancellation/ prepayment"),
                    "children_beds": house_rules.get("Children & Beds"),
                    "age_restriction": house_rules.get("Age restriction"),
                    "groups": house_rules.get("Groups"),
                    "pets": house_rules.get("Pets"),
                    "smoking": house_rules.get("Smoking"),
                    "cards_accepted": house_rules.get("Cards accepted at this hotel"),
                    "refundable_damage_deposit": house_rules.get(
                        "Refundable damage deposit"
                    ),
                    "hotel_id": hotel["id"],
                }
                if isinstance(house_rules, dict)
                else None
            )
            bulk_inserts_by_table[Hotel_House_Rules].append(hotel_house_rules)
            guest_reviews = hotel["guest_reviews"]
            hotel_guest_reviews = (
                [
                    {
                        "date": review.get("review_date"),
                        "title": review.get("review_title"),
                        "positive": review.get("positive"),
                        "negative": review.get("negative"),
                        "hotel_id": hotel["id"],
                    }
                    for review in guest_reviews
                    if review is not None
                ]
                if isinstance(guest_reviews, list)
                else []
            )
            bulk_inserts_by_table[Hotel_Guest_Reviews].extend(hotel_guest_reviews)
            hotel_location = {
                "city": hotel["city"],
                "address": hotel["address"],
                "hotel_id": hotel["id"],
            }
            bulk_inserts_by_table[Hotel_Location].append(hotel_location)
        tasks = []
        for model, entities in bulk_inserts_by_table.items():
            entities = [entity for entity in entities if entity is not None]
            tasks.append(
                insert_entities_into_database(
                    task_count=5, entities=entities, model=model
                )
            )
        await asyncio.gather(*tasks)
