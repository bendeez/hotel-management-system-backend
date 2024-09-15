import pandas as pd
from database import SessionLocal
from models import Hotels, Hotel_Rooms, Hotel_Location, Hotel_Review, Hotel_Guest_Reviews, Hotel_House_Rules
from data_cleaner.clean_hotel_data_tool import ht

df = pd.read_csv('./hotel_data/hotels_cleaned.csv')
df['amenities'] = df['amenities'].apply(ht.safe_literal_eval)
df["rooms_to_price"] = df["rooms_to_price"].apply(ht.safe_literal_eval).apply(ht.modify_room_to_price)

def sync_to_database():
    async with SessionLocal() as db:
        for index, hotel in df.iterrows():
            rooms_to_price = [ht.safe_literal_eval(room) for room in ht.safe_literal_eval(hotel['rooms_to_price'])]
            hotel_rooms = [Hotel_Rooms(room_type=ht.safe_literal_eval(room.get("room_type")),price=ht.safe_literal_eval(room.get("price")),
                                       guess_count=room.get("guess_count"))
                           for room in rooms_to_price if isinstance(room, dict)] if isinstance(rooms_to_price, list) else None
            hotel_review = Hotel_Review(subjective_rating=hotel["subjective_rating"],num_of_reviews=hotel["num_of_reviews"],
                                           staff_rating_out_of_10=hotel["staff_rating_out_of_10"], facilities_rating_out_of_10=hotel["facilities_rating_out_of_10"],
                                           cleanliness_rating_out_of_10=hotel["cleanliness_rating_out_of_10"],comfort_rating_out_of_10=hotel["comfort_rating_out_of_10"],
                                           value_for_money_rating_out_of_10=hotel["value_for_money_rating_out_of_10"],rating_out_of_10=hotel["rating_out_of_10"],
                                           location_rating_out_of_10=hotel["location_rating_out_of_10"],free_wifi_rating_out_of_10=hotel["free_wifi_rating_out_of_10"])

            house_rules = ht.safe_literal_eval(hotel["house_rules"])
            hotel_house_rules = Hotel_House_Rules(check_in=house_rules.get("Check-in"),
                                                  check_out=house_rules.get("Check-out"),
                                                  cancellation_payment=house_rules.get("Cancellation/ prepayment"),
                                                  children_beds=house_rules.get("Children & Beds"),
                                                  age_restriction=house_rules.get("No age restriction"),
                                                  groups=house_rules.get("Groups"),
                                                  cards_accepted=house_rules.get("Cards accepted at this hotel")) if isinstance(house_rules, dict) else None
            hotel_location = Hotel_Location(city=hotel["city"], address=hotel["address"])
            hotel_data = Hotels(title=hotel['title'], image_link=hotel["image_link"],
                                description=hotel['description'],amenities=ht.safe_literal_eval(hotel['amenities']),
                                hotel_rooms=hotel_rooms, hotel_review=hotel_review,
                                hotel_location=hotel_location, hotel_house_rules=hotel_house_rules)

