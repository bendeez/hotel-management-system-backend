from hotel_data.hotel_data_getter import get_hotel_data
from hotel_data.hotel_data_deleter import delete_hotel_data
import pandas as pd


async def test_sync_hotel_data_to_database(
    hotel_cleaned_df, modify_row_and_columns_for_consistent_ordering, hotel_data_syncer
):
    await hotel_data_syncer.sync_hotel_data_to_database(df=hotel_cleaned_df)
    hotel_data_from_db = await get_hotel_data()
    await delete_hotel_data()
    assert len(hotel_data_from_db) == len(hotel_cleaned_df)
    hotel_data_to_list = [
        {
            "title": h.title,
            "image_link": h.image_link,
            "description": h.description,
            "amenities": h.amenities,
            "rating_out_of_10": h.hotel_review.rating_out_of_10,
            "subjective_rating": h.hotel_review.subjective_rating,
            "num_of_reviews": h.hotel_review.num_of_reviews,
            "address": h.hotel_location.address,
            "city": h.hotel_location.city,
            "house_rules": {
                key: value
                for key, value in {
                    "Check-in": h.hotel_house_rules.check_in,
                    "Check-out": h.hotel_house_rules.check_out,
                    "Cancellation/ prepayment": h.hotel_house_rules.cancellation_payment,
                    "Children & Beds": h.hotel_house_rules.children_beds,
                    "Age restriction": h.hotel_house_rules.age_restriction,
                    "Pets": h.hotel_house_rules.pets,
                    "Groups": h.hotel_house_rules.groups,
                    "Cards accepted at this hotel": h.hotel_house_rules.cards_accepted,
                    "Smoking": h.hotel_house_rules.smoking,
                    "Refundable damage deposit": h.hotel_house_rules.refundable_damage_deposit,
                }.items()
                if value is not None
            },
            "rooms_to_price": [
                {
                    key: value
                    for key, value in {
                        "room_type": room.room_type,
                        "guest_count": room.guest_count,
                        "price": room.price,
                        "guest_count_numeric": room.guest_count_numeric,
                        "price_numeric": room.price_numeric,
                        "tax_and_fee_numeric": room.tax_and_fee_numeric,
                    }.items()
                    if value is not None
                }
                for room in h.hotel_rooms
            ],
            "guest_reviews": [
                {
                    "review_date": review.date,
                    "review_title": review.title,
                    "positive": review.positive,
                    "negative": review.negative,
                }
                for review in h.hotel_guest_reviews
            ],
            "staff_rating_out_of_10": h.hotel_review.staff_rating_out_of_10,
            "facilities_rating_out_of_10": h.hotel_review.facilities_rating_out_of_10,
            "cleanliness_rating_out_of_10": h.hotel_review.cleanliness_rating_out_of_10,
            "comfort_rating_out_of_10": h.hotel_review.comfort_rating_out_of_10,
            "value_for_money_rating_out_of_10": h.hotel_review.value_for_money_rating_out_of_10,
            "location_rating_out_of_10": h.hotel_review.location_rating_out_of_10,
            "free_wifi_rating_out_of_10": h.hotel_review.free_wifi_rating_out_of_10,
        }
        for h in hotel_data_from_db
    ]
    hotel_data_list_to_df = pd.DataFrame(hotel_data_to_list)
    hotel_data_list_to_df = modify_row_and_columns_for_consistent_ordering(
        df=hotel_data_list_to_df
    )
    pd.testing.assert_frame_equal(
        hotel_cleaned_df, hotel_data_list_to_df[hotel_cleaned_df.columns]
    )
