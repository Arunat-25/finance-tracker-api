import pytest_asyncio, pytest, asyncio, aiohttp
from aiohttp.test_utils import TestServer, TestClient
from aiohttp_asgi import ASGIResource

from sqlalchemy import text
from aiohttp import web

from tests.session import get_session, test_engine, test_session_factory


@pytest_asyncio.fixture(scope="function", autouse=True)
async def override_session_factory():
    from app.infrastructure.db import session as db_session

    original_session_factory = db_session.session_factory
    original_engine = db_session.engine

    db_session.session_factory = test_session_factory
    db_session.engine = test_engine

    yield

    db_session.session_factory = original_session_factory
    db_session.engine = original_engine


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db():
    from app.infrastructure.db.base_class import Base

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(scope="function")
async def session():
    session = await get_session().__anext__()
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def client():
    from app.main import app

    aiohttp_app = web.Application()
    asgi_resource = ASGIResource(app, root_path="/")
    aiohttp_app.router.register_resource(asgi_resource)

    server = TestServer(aiohttp_app)
    await server.start_server()

    async with TestClient(server) as client:
        yield client

    await server.close()