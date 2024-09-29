from app.tools.domain.base_repository import BaseRepository, JoinExpression
from app.hotel_app.hotels.domain.models import Hotels, Hotel_Location, Hotel_Review
from app.tools.domain.constants import DatabaseQueryOrder
from app.hotel_app.hotels.domain.constants import (
    HotelsAttributes,
    hotel_attributes_table_mapping,
)
from typing import Optional


class HotelsRepository(BaseRepository):
    async def get_all_hotels(
        self,
        limit: int,
        offset: int,
        order: DatabaseQueryOrder,
        order_by: HotelsAttributes,
        rating_lt: float,
        rating_gt: float,
        city: Optional[str] = None,
    ) -> list[Hotels]:
        join_relationships = [Hotels.hotel_review, Hotels.hotel_location]
        join_expressions = [
            JoinExpression(model=relationship, join_from=Hotels, outer=True)
            for relationship in join_relationships
        ]
        filters = [
            Hotel_Review.rating_out_of_10 >= rating_gt,
            Hotel_Review.rating_out_of_10 <= rating_lt,
        ]
        if city is not None:
            filters.append(Hotel_Location.city == city)
        order_by_model = hotel_attributes_table_mapping[order_by.value]
        hotels = await self._get_all(
            model=Hotels,
            joins=join_expressions,
            load_relationships=[
                Hotels.hotel_rooms,
                Hotels.hotel_house_rules,
                Hotels.hotel_guest_reviews,
            ],
            limit=limit,
            offset=offset,
            order=order,
            order_by=getattr(order_by_model, order_by.value),
            eager_load_relationships=join_relationships,
            filters=filters,
        )
        return hotels
