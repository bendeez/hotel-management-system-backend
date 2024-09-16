from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    declared_attr,
    as_declarative
)
from typing import Optional
from sqlalchemy import ForeignKey, Text, JSON

@as_declarative()
class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)



class Hotels(BaseMixin):
    title: Mapped[Optional[str]] = mapped_column(Text)
    image_link: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    amenities: Mapped[Optional[JSON]] = mapped_column(JSON)
    hotel_review: Mapped["Hotel_Review"] = relationship()
    hotel_rooms: Mapped[list["Hotel_Rooms"]] = relationship()
    hotel_house_rules: Mapped["Hotel_House_Rules"] = relationship()
    hotel_location: Mapped["Hotel_Location"] = relationship()
    hotel_guest_reviews: Mapped[list["Hotel_Guest_Reviews"]] = relationship()


class Hotel_Review(BaseMixin):
    rating_out_of_10: Mapped[Optional[float]]
    staff_rating_out_of_10: Mapped[Optional[float]]
    facilities_rating_out_of_10: Mapped[Optional[float]]
    cleanliness_rating_out_of_10: Mapped[Optional[float]]
    comfort_rating_out_of_10: Mapped[Optional[float]]
    value_for_money_rating_out_of_10: Mapped[Optional[float]]
    location_rating_out_of_10: Mapped[Optional[float]]
    free_wifi_rating_out_of_10: Mapped[Optional[float]]
    num_of_reviews: Mapped[Optional[int]]
    subjective_rating: Mapped[Optional[str]] = mapped_column(Text)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_Rooms(BaseMixin):
    room_type: Mapped[Optional[JSON]] = mapped_column(JSON)
    guest_count: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[Optional[JSON]] = mapped_column(JSON)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_House_Rules(BaseMixin):
    check_in: Mapped[Optional[str]] = mapped_column(Text)
    check_out: Mapped[Optional[str]] = mapped_column(Text)
    cancellation_payment: Mapped[Optional[str]] = mapped_column(Text)
    children_beds: Mapped[Optional[str]] = mapped_column(Text)
    age_restriction: Mapped[Optional[str]] = mapped_column(Text)
    pets: Mapped[Optional[str]] = mapped_column(Text)
    groups: Mapped[Optional[str]] = mapped_column(Text)
    cards_accepted: Mapped[Optional[str]] = mapped_column(Text)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_Location(BaseMixin):
    city: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_Guest_Reviews(BaseMixin):
    date: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(Text)
    positive: Mapped[Optional[str]] = mapped_column(Text)
    negative: Mapped[Optional[str]] = mapped_column(Text)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
