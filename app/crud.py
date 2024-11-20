from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from datetime import datetime


from .models import Office, Room, Booking, User
from .schemas import OfficeResponseCreate, RoomCreate, BookingCreate, UserCreate
from .auth import get_password_hash, verify_password, create_access_token
from typing import Optional

# Office CRUD
async def get_offices(
    db: AsyncSession, skip: int = 0, limit: int = 100, location: Optional[str] = None
):
    query = select(Office).offset(skip).limit(limit)
    if location:
        query = query.filter(Office.location == location)
    result = await db.execute(query)
    return result.scalars().all()


async def create_office(db: AsyncSession, office: OfficeResponseCreate):
    # Create a new office object
    db_office = Office(name=office.name, location=office.location)
    
    # Add the new office to the session
    db.add(db_office)
    
    # Commit the transaction asynchronously
    await db.commit()
    
    # Refresh the instance to retrieve its ID (after commit)
    await db.refresh(db_office)
    
    return db_office


# Room CRUD
async def get_rooms(
    db: AsyncSession, office_id: Optional[int] = None, capacity: Optional[int] = None
):
    query = select(Room)
    if office_id:
        query = query.filter(Room.office_id == office_id)
    if capacity:
        query = query.filter(Room.capacity == capacity)
    result = await db.execute(query)
    return result.scalars().all()


async def create_room(db: AsyncSession, room: RoomCreate):
    db_room = Room(name=room.name, capacity=room.capacity, office_id=room.office_id)
    db.add(db_room)
    await db.commit()
    return db_room


# Booking CRUD
async def get_bookings(
    db: AsyncSession, user_id: Optional[int] = None, room_id: Optional[int] = None
):
    query = select(Booking).options(selectinload(Booking.room))
    if user_id:
        query = query.filter(Booking.user_id == user_id)
    if room_id:
        query = query.filter(Booking.room_id == room_id)
    result = await db.execute(query)
    return result.scalars().all()


async def create_booking(db: AsyncSession, booking: BookingCreate):
    # Check if room is already booked for the requested time
    conflicting_booking = await db.execute(
        select(Booking).filter(
            Booking.room_id == booking.room_id,
            Booking.start_time < booking.end_time,
            Booking.end_time > booking.start_time,
        )
    )
    if conflicting_booking.scalar():
        raise ValueError("Room is already booked for this time.")

    db_booking = Booking(
        room_id=booking.room_id,
        user_id=booking.user_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
    )
    db.add(db_booking)
    await db.commit()
    return db_booking


# User CRUD
async def create_user(db: AsyncSession, user_create: UserCreate):
    hashed_password = auth.hash_password(user_create.password)
    db_user = User(username=user_create.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.scalars().first()

async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
