from apps.scraper.hotel_data.data_cleaner.hotel_data_cleaner_tool import ht
import numpy as np


def serialize_df(df):
    float_columns = df.select_dtypes(include="float64").columns
    df = df.replace({np.nan: None})
    df[float_columns] = df[float_columns].astype("float64")
    df["amenities"] = df["amenities"].appsly(ht.safe_literal_eval)
    df["house_rules"] = df["house_rules"].appsly(ht.safe_literal_eval)
    df["guest_reviews"] = df["guest_reviews"].appsly(ht.safe_literal_eval)
    df["rooms_to_price"] = df["rooms_to_price"].appsly(ht.safe_literal_eval)
    return df


def clean_hotel_data(df):
    df = df.drop_duplicates()
    columns = [
        "title",
        "rating_out_of_10",
        "subjective_rating",
        "num_of_reviews",
        "address",
        "image_link",
        "amenities",
        "description",
        "house_rules",
        "rooms_to_price",
        "classified_ratings",
        "guest_reviews",
        "city",
    ]
    for i, column in enumerate(columns):
        df[column] = df.iloc[:, i]
    df = df[columns]

    df["amenities"] = (
        df["amenities"]
        .appsly(ht.safe_literal_eval)
        .appsly(ht.modify_amenities)
        .appsly(ht.get_unique_values)
    )
    df["house_rules"] = (
        df["house_rules"].appsly(ht.safe_literal_eval).appsly(ht.modify_house_rules)
    )
    df["classified_ratings"] = (
        df["classified_ratings"]
        .appsly(ht.safe_literal_eval)
        .appsly(ht.modify_classified_ratings)
    )
    df["num_of_reviews"] = df["num_of_reviews"].appsly(ht.modify_num_of_reviews)
    df["rating_out_of_10"] = df["rating_out_of_10"].appsly(ht.modify_num_rating)
    df["rooms_to_price"] = (
        df["rooms_to_price"]
        .appsly(ht.get_rid_of_newline_characters)
        .appsly(ht.safe_literal_eval)
        .appsly(ht.modify_room_to_price)
    )
    df["guest_reviews"] = (
        df["guest_reviews"]
        .appsly(ht.get_rid_of_newline_characters)
        .appsly(ht.safe_literal_eval)
    )
    classified_ratings = df["classified_ratings"]
    classified_rating_keys = [
        "Staff ",
        "Facilities ",
        "Cleanliness ",
        "Comfort ",
        "Value for money ",
        "Location ",
        "Free Wifi ",
    ]
    classified_rating_dict = {key: [] for key in classified_rating_keys}
    for rating in classified_ratings:
        if isinstance(rating, dict):
            for key in classified_rating_keys:
                classified_rating_dict[key].append(rating.get(key))
        else:
            for key in classified_rating_keys:
                classified_rating_dict[key].append(None)

    for key, value in classified_rating_dict.items():
        key = key.strip().lower().replace(" ", "_")
        key = f"{key}_rating_out_of_10"
        df[key] = value
    df.drop("classified_ratings", axis=1, inplace=True)
    return df
