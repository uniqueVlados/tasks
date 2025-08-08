
from pydantic import BaseModel, Field


class PersonBase(BaseModel):
    phone: str
    fullname: str
    amount: str
    rating: int

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    amount: float
    
    class Config:
        orm_mode = True

