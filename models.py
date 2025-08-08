
from sqlalchemy import Column, Integer, String, Float

from database import Base


class DBPerson(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    fullname = Column(String)
    amount = Column(Float)
    rating = Column(Integer)