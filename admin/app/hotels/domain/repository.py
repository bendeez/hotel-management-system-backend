from app.tools.domain.base_repository import BaseRepository, JoinExpression
from app.hotels.domain.models import Hotels
from app.tools.domain.constants import DatabaseQueryOrder
from app.hotels.domain.constants import HotelsAttributes, hotel_attributes_table_mapping


class HotelsRepository(BaseRepository):
    async def get_all_hotels(
        self,
        limit: int,
        offset: int,
        order: DatabaseQueryOrder,
        order_by: HotelsAttributes,
    ) -> list[Hotels]:
        join_relationships = [Hotels.hotel_review, Hotels.hotel_location]
        order_by_model = hotel_attributes_table_mapping[order_by.value]
        hotels = await self._get_all(
            model=Hotels,
            joins=[
                JoinExpression(model=relationship, join_from=Hotels, outer=True)
                for relationship in join_relationships
            ],
            relationships=[
                Hotels.hotel_rooms,
                Hotels.hotel_house_rules,
                Hotels.hotel_guest_reviews,
            ],
            limit=limit,
            offset=offset,
            order=order,
            order_by=getattr(order_by_model, order_by.value),
            eager_load_relationships=join_relationships,
        )
        return hotels
