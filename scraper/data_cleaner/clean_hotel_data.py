import pandas as pd
from clean_hotel_data_tool import ht

df = pd.read_csv("hotels_copy.csv")
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
    .apply(ht.safe_literal_eval)
    .apply(ht.modify_amenities)
    .apply(ht.get_unique_values)
)
df["classified_ratings"] = (
    df["classified_ratings"]
    .apply(ht.safe_literal_eval)
    .apply(ht.modify_classified_ratings)
)
df["num_of_reviews"] = df["num_of_reviews"].apply(ht.modify_num_of_reviews)
df["rating_out_of_10"] = df["rating_out_of_10"].apply(ht.modify_num_rating)
df["rooms_to_price"] = (
    df["rooms_to_price"]
    .apply(ht.get_rid_of_newline_characters)
    .apply(ht.safe_literal_eval)
    .apply(ht.modify_room_to_price)
)
classified_ratings = df["classified_ratings"]
classified_rating_keys = list(classified_ratings[15].keys())
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
df.to_csv("hotels_cleaned.csv", index=False)
