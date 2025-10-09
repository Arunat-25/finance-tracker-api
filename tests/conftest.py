import pytest_asyncio, pytest, asyncio, aiohttp
from sqlalchemy.ext.asyncio import create_async_engine

from app.common.config import settings
from tests.session import get_session
from app.db.base_class import Base



@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def session():
    """Create a fresh database session for each test"""
    async for session in get_session():
        yield session
        break

@pytest.fixture(scope="function")
async def client():
    """Create a new aiohttp client session for each test"""
    async with aiohttp.ClientSession() as client:
        yield client
