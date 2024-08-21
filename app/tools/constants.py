from enum import Enum


class DatabaseQueryOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class DatabaseQueryQuantity(Enum):
    FIRST = "first"
    ALL = "all"


def get_enum_by_value(enum, value):
    for e in enum:
        if e.value == value:
            return e
    return None
