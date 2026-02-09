import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.adapters.db.models import Base
from src.config.settings import settings

# Use a test database if possible, or just the same one if in a controlled environment
# For this task, I'll assume we can use the configured one or it's mocked
TEST_DATABASE_URL = settings.DATABASE_URL # Could be changed to a test db

engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        # For tests, we might want to recreate the schema
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        pass

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()
