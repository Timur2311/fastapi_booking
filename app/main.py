from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from app import database, schemas, crud, auth
from typing import Optional, Union
from sqlalchemy.future import select
from fastapi_pagination import add_pagination
from app.schemas import DeleteResponse
from app.database import get_db
from app.models import Office, Room, Booking
from .admin import init_admin
from app.models import User
import sentry_sdk
from app.settings import SENTRY_DSN

app = FastAPI()

# Setup admin panel
init_admin(app)

@app.post("/offices/", response_model=schemas.OfficeResponse)
async def create_office(
    office: schemas.OfficeResponseCreate, db: AsyncSession = Depends(database.get_db)
):

    query = select(Office).filter(Office.name == office.name)
    result = await db.execute(query)

    # Fetch all matching offices
    existing_offices = result.scalars().all()

    if existing_offices:
        # If any office with the same name exists, raise a 409 Conflict error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Office with this name already exists.",
        )
    return await crud.create_office(db=db, office=office)


@app.get("/offices/", response_model=Page[schemas.OfficeResponse])
async def get_offices(
    skip: int = 0,
    limit: int = 100,
    location: Optional[str] = None,
    db: AsyncSession = Depends(database.get_db),
):
    return paginate(
        await crud.get_offices(db=db, skip=skip, limit=limit, location=location)
    )




# Retrieve an office by its ID
@app.get("/offices/{office_id}", response_model=schemas.OfficeResponse)
async def get_office(office_id: int, db: AsyncSession = Depends(get_db)) -> Office:
    query = select(Office).filter(Office.id == office_id)
    result = await db.execute(query)
    office = result.scalar_one_or_none()
    if office is None:
        raise HTTPException(status_code=404, detail="Office not found")
    return office


# Update an office by its ID
@app.put("/offices/{office_id}", response_model=schemas.OfficeResponse)
async def update_office(
    office_id: int, office: schemas.OfficeResponseCreate, db: AsyncSession = Depends(get_db)
):
    query = select(Office).filter(Office.id == office_id)
    result = await db.execute(query)
    db_office = result.scalar_one_or_none()

    if db_office is None:
        raise HTTPException(status_code=404, detail="Office not found")

    db_office.name = office.name
    db_office.location = office.location

    await db.commit()
    await db.refresh(db_office)
    return db_office


# Delete an office by its ID
@app.delete("/offices/{office_id}", response_model=DeleteResponse)
async def delete_office(office_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Office).filter(Office.id == office_id)
    result = await db.execute(query)
    db_office = result.scalar_one_or_none()

    if db_office is None:
        raise HTTPException(status_code=404, detail="Office not found")

    await db.delete(db_office)
    await db.commit()
    return DeleteResponse(message="Office successfully deleted")


@app.post("/rooms/", response_model=schemas.Room)
async def create_room(
    room: schemas.RoomCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_room(db=db, room=room)


@app.get("/rooms/", response_model=Page[schemas.Room])
async def get_rooms(
    office_id: Optional[int] = None,
    capacity: Optional[int] = None,
    db: AsyncSession = Depends(database.get_db),
):
    return paginate(await crud.get_rooms(db=db, office_id=office_id, capacity=capacity))


# Retrieve a room by its ID
@app.get("/rooms/{room_id}", response_model=Union[schemas.Room, dict, None])
async def get_room(room_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Room).filter(Room.id == room_id)
    result = await db.execute(query)
    room = result.scalar_one_or_none()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


# Update a room by its ID
@app.put("/rooms/{room_id}", response_model=schemas.Room)
async def update_room(
    room_id: int, room: schemas.RoomCreate, db: AsyncSession = Depends(get_db)
):
    query = select(Room).filter(Room.id == room_id)
    result = await db.execute(query)
    db_room = result.scalar_one_or_none()

    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    db_room.name = room.name
    db_room.capacity = room.capacity
    db_room.office_id = room.office_id

    await db.commit()
    await db.refresh(db_room)
    return db_room


# Delete a room by its ID
@app.delete("/rooms/{room_id}", response_model=DeleteResponse)
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Room).filter(Room.id == room_id)
    result = await db.execute(query)
    db_room = result.scalar_one_or_none()

    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    await db.delete(db_room)
    await db.commit()
    return DeleteResponse(message="Room successfully deleted")



@app.post("/bookings/", response_model=schemas.Booking)
async def create_booking(
    booking: schemas.BookingCreate, db: AsyncSession = Depends(database.get_db)
):
    try:
        return await crud.create_booking(db=db, booking=booking)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/bookings/", response_model=Page[schemas.BookingList])
async def get_bookings(
    user_id: Optional[int] = None,
    room_id: Optional[int] = None,
    db: AsyncSession = Depends(database.get_db),
):
    return paginate(await crud.get_bookings(db=db, user_id=user_id, room_id=room_id))


# Retrieve a booking by its ID
@app.get("/bookings/{booking_id}", response_model=Union[schemas.Booking, dict, None])
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Booking).filter(Booking.id == booking_id)
    result = await db.execute(query)
    booking = result.scalar_one_or_none()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


# Update a booking by its ID
@app.put("/bookings/{booking_id}", response_model=schemas.Booking)
async def update_booking(
    booking_id: int, booking: schemas.BookingCreate, db: AsyncSession = Depends(get_db)
):
    query = select(Booking).filter(Booking.id == booking_id)
    result = await db.execute(query)
    db_booking = result.scalar_one_or_none()

    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    db_booking.room_id = booking.room_id
    db_booking.user_id = booking.user_id
    db_booking.start_time = booking.start_time
    db_booking.end_time = booking.end_time

    await db.commit()
    await db.refresh(db_booking)
    return db_booking


# Delete a booking by its ID
@app.delete("/bookings/{booking_id}", response_model=DeleteResponse)
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Booking).filter(Booking.id == booking_id)
    result = await db.execute(query)
    db_booking = result.scalar_one_or_none()

    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    await db.delete(db_booking)
    await db.commit()
    return DeleteResponse(message="Booking successfully deleted")



@app.post("/auth/register", response_model=schemas.User)
async def register_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)
):
    # Check if user already exists
    query = select(User).filter(User.username == user.username)
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Hash password before saving
    hashed_password = auth.hash_password(user.password)

    # Create the user and add to the database
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()

    return new_user


@app.post("/auth/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)
):
    user = await crud.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/items/")
# async def read_items(db: AsyncSession = Depends(get_db_session)):
#     result = await db.execute("SELECT * FROM items")
#     items = result.fetchall()
#     return {"items": items}


add_pagination(app)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0