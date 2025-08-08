from enum import Enum
from pydantic import BaseModel


class Person(BaseModel):
    phone: str
    fullname: str
    amount: str
    rating: int


class PersonOut(Person):
    amount: float


class SortField(str, Enum):
    phone = "phone"
    fullname = "fullname"
    amount = "amount"
    rating = "rating"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
