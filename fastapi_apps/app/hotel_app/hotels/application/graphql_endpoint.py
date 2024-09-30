import strawberry
from strawberry.fastapi import GraphQLRouter
from app.hotel_app.hotels.domain.schemas import HotelsOut
from app.hotel_app.hotels.application.dependencies import get_hotels_service
from fastapi import Query, Depends
from app.hotel_app.hotels.domain.service import HotelsService
from app.hotel_app.hotels.domain.schemas import (
    HotelReviewOut,
    HotelRoomsOut,
    HotelHouseRulesOut,
    HotelLocationOut,
    HotelGuestReviewsOut,
    HotelsOut,
)
from app.hotel_app.hotels.domain.constants import HotelsAttributes
from app.tools.domain.constants import DatabaseQueryOrder
from typing import List, Optional
from pydantic import Field

StrawberryDatabaseQueryOrder = strawberry.enum(DatabaseQueryOrder)
StrawberryHotelsAttributes = strawberry.enum(HotelsAttributes)


@strawberry.experimental.pydantic.type(model=HotelReviewOut, all_fields=True)
class HotelReview:
    pass


@strawberry.experimental.pydantic.type(model=HotelRoomsOut, all_fields=True)
class HotelRooms:
    pass


@strawberry.experimental.pydantic.type(model=HotelHouseRulesOut, all_fields=True)
class HotelHouseRules:
    pass


@strawberry.experimental.pydantic.type(model=HotelLocationOut, all_fields=True)
class HotelLocation:
    pass


@strawberry.experimental.pydantic.type(model=HotelGuestReviewsOut, all_fields=True)
class HotelGuestReviews:
    pass


@strawberry.experimental.pydantic.type(model=HotelsOut)
class Hotels:
    id: int
    title: Optional[str] = None
    image_link: Optional[str] = None
    description: Optional[str] = None
    amenities: List[str] = Field(default_factory=list)
    hotel_review: Optional[HotelReview] = None
    hotel_rooms: List[HotelRooms] = Field(default_factory=list)
    hotel_house_rules: Optional[HotelHouseRules] = None
    hotel_location: Optional[HotelLocation] = None
    hotel_guest_reviews: List[HotelGuestReviews] = Field(default_factory=list)


async def get_context(hotels_service: HotelsService = Depends(get_hotels_service)):
    return {"hotels_service": hotels_service}


async def get_all_hotels(
    info: strawberry.Info,
    city: Optional[str] = None,
    limit: int = Query(default=100, le=100),
    offset: int = 0,
    order_by: StrawberryHotelsAttributes = StrawberryHotelsAttributes.ID,
    order: StrawberryDatabaseQueryOrder = StrawberryDatabaseQueryOrder.DESC,
    rating_gt: float = Query(default=None, le=10),
    rating_lt: float = Query(default=None, ge=0),
) -> List[Hotels]:
    hotels_service = info.context["hotels_service"]
    hotels = await hotels_service.get_all_hotels(
        limit=limit,
        offset=offset,
        order_by=order_by,
        order=order,
        city=city,
        rating_gt=rating_gt,
        rating_lt=rating_lt,
    )
    return hotels


@strawberry.type
class Query:
    hotels: List[Hotels] = strawberry.field(resolver=get_all_hotels)


schema = strawberry.Schema(Query)

hotel_router = GraphQLRouter(
    schema=schema, context_getter=get_context, prefix="/hotels"
)
