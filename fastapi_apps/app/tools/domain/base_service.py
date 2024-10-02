from sqlalchemy.sql.elements import BinaryExpression, Null


class BaseService:
    def _filter_out_null_comparisons(
        self, filters: list[BinaryExpression]
    ) -> list[BinaryExpression]:
        return [f for f in filters if f is not None and not isinstance(f.right, Null)]
