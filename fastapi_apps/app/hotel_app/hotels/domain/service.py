from app.hotel_app.hotels.domain.repository import HotelsRepository
from app.tools.domain.constants import DatabaseQueryOrder
from app.hotel_app.hotels.domain.constants import HotelsAttributes
from app.tools.domain.base_service import BaseService
from app.hotel_app.hotels.domain.models import Hotel_Location, Hotel_Review
from app.hotel_app.hotels.domain.exceptions import HotelsOverflow, InvalidComparision
from typing import Optional


class HotelsService(BaseService):
    def __init__(self, repository: HotelsRepository):
        self.repository = repository

    async def get_all_hotels(
        self,
        limit: int,
        offset: int,
        order: DatabaseQueryOrder,
        order_by: HotelsAttributes,
        rating_lt: Optional[float] = None,
        rating_gt: Optional[float] = None,
        num_of_reviews_gt: Optional[float] = None,
        num_of_reviews_lt: Optional[float] = None,
        city: Optional[str] = None,
    ):
        if limit > 500:
            raise HotelsOverflow()
        if (
            num_of_reviews_gt
            and num_of_reviews_lt
            and (num_of_reviews_gt > num_of_reviews_lt)
        ):
            raise InvalidComparision()
        if rating_gt and rating_lt and (rating_gt > rating_lt):
            raise InvalidComparision()
        filters = self._filter_out_null_comparisons(
            [
                Hotel_Review.rating_out_of_10 >= rating_gt
                if rating_gt is not None
                else None,
                Hotel_Review.rating_out_of_10 <= rating_lt
                if rating_lt is not None
                else None,
                Hotel_Location.city == city,
                Hotel_Review.num_of_reviews <= num_of_reviews_lt
                if num_of_reviews_lt is not None
                else None,
                Hotel_Review.num_of_reviews >= num_of_reviews_gt
                if num_of_reviews_gt is not None
                else None,
            ]
        )
        hotels = await self.repository.get_all_hotels(
            limit=limit, offset=offset, order=order, order_by=order_by, filters=filters
        )
        return hotels
