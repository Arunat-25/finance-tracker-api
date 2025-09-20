import pytest_asyncio, pytest, asyncio
from tests.session import session_factory



# @pytest.fixture(scope="session")
# def event_loop():
#     """Создаем event loop на всю сессию тестов"""
#     try:
#         policy = asyncio.WindowsProactorEventLoopPolicy()
#         asyncio.set_event_loop_policy(policy)
#     except AttributeError:
#         pass
#
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with session_factory() as sess:
        async with sess.begin():
            try:
                yield sess
            finally:
                await sess.close()

