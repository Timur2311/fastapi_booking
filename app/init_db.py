import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select

from database import engine  
from models import Base 

# Function to initialize the database
async def init_db():
    # Create all tables in the database
    async with engine.begin() as conn:
        # Create all tables defined in the Base metadata
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized!")

# Run the initialization
if __name__ == "__main__":
    asyncio.run(init_db())
