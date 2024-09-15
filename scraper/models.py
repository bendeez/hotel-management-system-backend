from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declared_attr,
    as_declarative,
    relationship,
)
from typing import Optional
from sqlalchemy import ForeignKey, String, JSON


@as_declarative()
class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class Hotels(BaseMixin):
    title: Mapped[Optional[str]] = mapped_column(String(500))
    image_link: Mapped[Optional[str]] = mapped_column(String(500))
    description: Mapped[Optional[str]] = mapped_column(String(5000))
    amenities: Mapped[Optional[list]] = mapped_column(JSON)
    hotel_review: Mapped["Hotel_Review"] = relationship()
    hotel_rooms: Mapped[list["Hotel_Rooms"]] = relationship()
    hotel_house_rules: Mapped[list["Hotel_House_Rules"]] = relationship()
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
    subjective_rating: Mapped[Optional[str]] = mapped_column(String(500))
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_Rooms(BaseMixin):
    room_type: Mapped[Optional[list]] = mapped_column(JSON)
    guest_count: Mapped[Optional[str]] = mapped_column(String(500))
    price: Mapped[Optional[list]] = mapped_column(JSON)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_House_Rules(BaseMixin):
    check_in: Mapped[Optional[str]] = mapped_column(String(1000))
    check_out: Mapped[Optional[str]] = mapped_column(String(1000))
    cancellation_payment: Mapped[Optional[str]] = mapped_column(String(1000))
    children_beds: Mapped[Optional[str]] = mapped_column(String(1000))
    age_restriction: Mapped[Optional[str]] = mapped_column(String(1000))
    pets: Mapped[Optional[str]] = mapped_column(String(1000))
    groups: Mapped[Optional[str]] = mapped_column(String(1000))
    cards_accepted: Mapped[Optional[str]] = mapped_column(String(1000))
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_Location(BaseMixin):
    city: Mapped[Optional[str]] = mapped_column(String(500))
    address: Mapped[Optional[str]] = mapped_column(String(500))
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))


class Hotel_Guest_Reviews(BaseMixin):
    date: Mapped[Optional[str]] = mapped_column(String(500))
    title: Mapped[Optional[str]] = mapped_column(String(500))
    positive: Mapped[Optional[str]] = mapped_column(String(500))
    negative: Mapped[Optional[str]] = mapped_column(String(500))
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
