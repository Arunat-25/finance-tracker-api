import pytest_asyncio, pytest, asyncio

from tests.session import session_factory
from app.db.base_class import Base

from tests.session import test_engine


@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with session_factory() as sess:
        async with sess.begin():
            try:
                yield sess
            finally:
                await sess.close()

