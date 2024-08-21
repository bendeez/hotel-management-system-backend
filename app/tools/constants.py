from enum import Enum


class DatabaseQueryOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class DatabaseQueryQuantity(Enum):
    FIRST = "first"
    ALL = "all"
