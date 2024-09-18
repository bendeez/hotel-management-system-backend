from hotel_data.data_cleaner.hotel_data_cleaner import clean_hotel_data
import pandas as pd


def test_cleaned_hotel_data(hotel_cleaned_df, hotel_uncleaned_df, sort_guest_reviews):
    cleaned_hotel_data = clean_hotel_data(df=hotel_uncleaned_df)
    cleaned_hotel_data["amenities"] = cleaned_hotel_data["amenities"].apply(sorted)
    cleaned_hotel_data["house_rules"] = cleaned_hotel_data["house_rules"].apply(
        lambda v: dict(sorted(v.items()))
    )
    cleaned_hotel_data["guest_reviews"] = (
        cleaned_hotel_data["guest_reviews"]
        .apply(lambda values: [dict(sorted(v.items())) for v in values])
        .apply(sort_guest_reviews)
    )
    pd.testing.assert_frame_equal(cleaned_hotel_data, hotel_cleaned_df)
