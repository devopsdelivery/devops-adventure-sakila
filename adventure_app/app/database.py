from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/appdb"

# Create an async engine instance
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base: DeclarativeMeta = declarative_base()

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
