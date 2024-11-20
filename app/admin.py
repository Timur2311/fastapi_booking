from sqladmin import Admin, ModelView
from fastapi import FastAPI
from .database import engine
from .models import Office, Room, Booking, User  # Import your models

# Create views for your models
class OfficeAdmin(ModelView, model=Office):
    column_list = [Office.id, Office.name, Office.location]

class RoomAdmin(ModelView, model=Room):
    column_list = [Room.id, Room.name, Room.capacity, Room.office_id]

class BookingAdmin(ModelView, model=Booking):
    column_list = [Booking.id, Booking.room_id, Booking.user_id, Booking.start_time, Booking.end_time]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]

# Add Admin instance
def init_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(OfficeAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(BookingAdmin)
    admin.add_view(UserAdmin)
