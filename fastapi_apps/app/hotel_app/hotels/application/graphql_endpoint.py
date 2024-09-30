import strawberry
from strawberry.fastapi import GraphQLRouter
from app.hotel_app.hotels.domain.schemas import HotelsOut
from app.hotel_app.hotels.application.dependencies import get_hotels_service
from fastapi import Depends
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
from app.hotel_app.hotels.domain.models import Hotels
from app.tools.domain.constants import DatabaseQueryOrder
from typing import List, Optional

DatabaseQueryOrderGQL = strawberry.enum(DatabaseQueryOrder)
HotelsAttributesGQL = strawberry.enum(HotelsAttributes)


@strawberry.experimental.pydantic.type(model=HotelReviewOut, all_fields=True)
class HotelReviewGQL:
    pass


@strawberry.experimental.pydantic.type(model=HotelRoomsOut, all_fields=True)
class HotelRoomsGQL:
    pass


@strawberry.experimental.pydantic.type(model=HotelHouseRulesOut, all_fields=True)
class HotelHouseRulesGQL:
    pass


@strawberry.experimental.pydantic.type(model=HotelLocationOut, all_fields=True)
class HotelLocationGQL:
    pass


@strawberry.experimental.pydantic.type(model=HotelGuestReviewsOut, all_fields=True)
class HotelGuestReviewsGQL:
    pass


@strawberry.experimental.pydantic.type(model=HotelsOut, all_fields=True)
class HotelsGQL:
    pass


async def get_context(hotels_service: HotelsService = Depends(get_hotels_service)):
    return {"hotels_service": hotels_service}


def transform_hotel_models_to_gql(hotels: List[Hotels]) -> List[HotelsGQL]:
    hotels_to_pydantic = [HotelsOut.model_validate(hotel) for hotel in hotels]
    hotels_to_gql = [
        HotelsGQL(
            **hotel.model_dump(
                exclude={
                    "hotel_review",
                    "hotel_rooms",
                    "hotel_house_rules",
                    "hotel_location",
                    "hotel_guest_reviews",
                }
            ),
            hotel_review=HotelReviewGQL(**hotel.hotel_review.model_dump())
            if hotel.hotel_review
            else None,
            hotel_rooms=[
                HotelRoomsGQL(**room.model_dump()) for room in hotel.hotel_rooms
            ]
            if hotel.hotel_rooms
            else [],
            hotel_house_rules=HotelHouseRulesGQL(**hotel.hotel_house_rules.model_dump())
            if hotel.hotel_house_rules
            else None,
            hotel_location=HotelLocationGQL(**hotel.hotel_location.model_dump())
            if hotel.hotel_location
            else None,
            hotel_guest_reviews=[
                HotelGuestReviewsGQL(**guest_review.model_dump())
                for guest_review in hotel.hotel_guest_reviews
            ]
            if hotel.hotel_guest_reviews
            else [],
        )
        for hotel in hotels_to_pydantic
    ]
    return hotels_to_gql


async def get_all_hotels(
    info: strawberry.Info,
    city: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
    order_by: HotelsAttributesGQL = HotelsAttributesGQL.ID,
    order: DatabaseQueryOrderGQL = DatabaseQueryOrderGQL.DESC,
    rating_gt: Optional[float] = None,
    rating_lt: Optional[float] = None,
) -> List[HotelsGQL]:
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
    hotels_gql = transform_hotel_models_to_gql(hotels=hotels)
    return hotels_gql


@strawberry.type
class Query:
    hotels: List[HotelsGQL] = strawberry.field(resolver=get_all_hotels)


schema = strawberry.Schema(Query)

hotel_router = GraphQLRouter(
    schema=schema, context_getter=get_context, prefix="/hotels"
)
