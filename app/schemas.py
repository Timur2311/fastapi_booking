from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class RoomBase(BaseModel):
    name: str
    capacity: Optional[int] = None


class RoomCreate(RoomBase):
    office_id: int


class Room(RoomBase):
    id: int
    office_id: int

    class Config:
        orm_mode = True




class OfficeBase(BaseModel):
    name: str
    location: str


class OfficeResponse(OfficeBase):
    id: int

    class Config:
        orm_mode = True


class UpdateOfficeResponse(OfficeBase):
    id: int
    rooms: List[Room]

    class Config:
        orm_mode = True


class OfficeResponseCreate(OfficeBase):
    pass


class BookingBase(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime


class BookingCreate(BookingBase):
    room_id: int


class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True
        
class BookingList(BookingBase):
    id: int
    room_id: int
    class Config:
        orm_mode = True


# DeleteResponse
class DeleteResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True


# User schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
