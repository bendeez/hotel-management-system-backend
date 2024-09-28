from enum import Enum
from app.hotel_app.domain.models import Hotels, Hotel_Review, Hotel_Location


class HotelsAttributes(Enum):
    ID = "id"
    TITLE = "title"
    NUM_OF_REVIEWS = "num_of_reviews"
    RATING_OUT_OF_10 = "rating_out_of_10"
    CITY = "city"


hotel_attributes_table_mapping = {
    HotelsAttributes.ID.value: Hotels,
    HotelsAttributes.TITLE.value: Hotels,
    HotelsAttributes.NUM_OF_REVIEWS.value: Hotel_Review,
    HotelsAttributes.RATING_OUT_OF_10.value: Hotel_Review,
    HotelsAttributes.CITY.value: Hotel_Location,
}
