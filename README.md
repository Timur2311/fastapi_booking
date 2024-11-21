# SIMPLE FASTAPI BOOKING SYSTEM

This is a FastAPI project using **SQLAlchemy** for database interactions and **SQLAdmin** for an admin interface. The project is set up with **Docker** for running PostgreSQL as the database.

---

## Features

- **FastAPI**: A high-performance web framework for building APIs.
- **SQLAlchemy**: An ORM for database interaction.
- **SQLAdmin**: An admin interface for managing your data.
- **Docker**: Simplified database setup and deployment.
- **Asynchronous Operations**: Optimized with `asyncpg` and `SQLAlchemy`.

---

## Requirements

- Python 3.12 or higher
- Docker and Docker Compose

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Timur2311/fastapi_booking.git
cd fastapi_booking


### 2. Create and activate a virtual environment
- On macOS and Linux:

python3 -m venv venv
source venv/bin/activate

- On Windows:

python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure environment variables

- Create a .env file in the project root with the following content:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app_db
SECRET_KEY="'i=.zBs[XfAu.E4N|yl98,q'h5#XJd"

#load the environment variables
source .env

### 5. Run PostgreSQL with Docker

- Start the database using Docker Compose:

docker-compose up -d

### 6. Initialize the database

- Run the app/init_db.py script to create database tables:

python app/init_db.py

### 7. Run the FastAPI application
uvicorn app.main:app --reload


- Admin Panel
- Access the SQLAdmin panel at:

http://127.0.0.1:8000/admin

- Swagger:
http://127.0.0.1:8000/docs

