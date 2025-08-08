from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List

from database import get_db
from models import DBPerson
from schemas import PersonCreate, Person
from functions import normalize_phone, normalize_fullname, normalize_amount

router = APIRouter()

@router.post("", response_model=Person, status_code=status.HTTP_201_CREATED)
async def create_person(person: PersonCreate,  db: AsyncSession = Depends(get_db)):
        normalized_phone = normalize_phone(person.phone)
        normalized_fullname = normalize_fullname(person.fullname)
        normalized_amount = normalize_amount(person.amount)
        
        existing_person = await db.execute(select(DBPerson).where(DBPerson.phone == normalized_phone))
        if existing_person.scalar():
            raise HTTPException(
                status_code=400,
                detail="Person with this phone already exists"
            )
        
        db_person = DBPerson(
            phone=normalized_phone,
            fullname=normalized_fullname,
            amount=normalized_amount,
            rating=person.rating
        )
        
        db.add(db_person)
        await db.commit()
        await db.refresh(db_person)
        
        return db_person
    
@router.get("", response_model=List[Person])
async def read_persons(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBPerson).offset(skip).limit(limit))
    persons = result.scalars().all()
    return persons
    
@router.get("/{person_id}", response_model=Person)
async def read_person(person_id: int, db: AsyncSession = Depends(get_db)):
    db_person = await db.get(DBPerson, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person
    
@router.put("/{person_id}", response_model=Person)
async def update_person(person_id: int, person: PersonCreate, db: AsyncSession = Depends(get_db)):
    db_person = await db.get(DBPerson, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    
    normalized_phone = normalize_phone(person.phone)
    normalized_fullname = normalize_fullname(person.fullname)
    normalized_amount = normalize_amount(person.amount)
    
    if db_person.phone != normalized_phone:
        existing_person = await db.execute(
            select(DBPerson).where(DBPerson.phone == normalized_phone))
        if existing_person.scalar():
            raise HTTPException(
                status_code=400,
                detail="Person with this phone already exists"
            )
    
    db_person.phone = normalized_phone
    db_person.fullname = normalized_fullname
    db_person.some_amount = normalized_amount
    db_person.rating_position = person.rating
    
    await db.commit()
    await db.refresh(db_person)
        
    return db_person
    
@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(person_id: int, db: AsyncSession = Depends(get_db)):
    db_person = await db.get(DBPerson, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    
    await db.delete(db_person)
    await db.commit()
    
    return None