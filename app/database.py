from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.settings import DATABASE_URL

# Create an asynchronous database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker that generates AsyncSession objects
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Dependency that provides a database session for each request
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
