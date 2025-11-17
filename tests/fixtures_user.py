import aiohttp, pytest_asyncio

from sqlalchemy import select, delete

from app.repositories.user import create_user
from app.common.config import settings
from app.infrastructure.models.user import UserOrm
from app.schemas.user import UserCreate



@pytest_asyncio.fixture(scope="function")
async def create_user_for_test(db_session):
    stmt = select(UserOrm).where(UserOrm.email == "test@gmail.com")
    res = await db_session.execute(stmt)
    existing_user = res.scalar_one_or_none()

    if existing_user:
        test_user = existing_user
    else:
        test_user = UserCreate(name="test_user", email="test@gmail.com", password="test_password")
        test_user = await create_user(db_session, test_user)
        await db_session.commit()
        await db_session.refresh(test_user)
    return test_user



@pytest_asyncio.fixture(scope="function")
async def delete_test_user(db_session):
    yield

    try:
        await db_session.execute(
            delete(UserOrm).where(UserOrm.email == "test@gmail.com")
        )
        await db_session.commit()
    except Exception:
        await db_session.rollback()


@pytest_asyncio.fixture(scope="function")
async def do_post_request_to_create_user():
    payload = {
        "name": "test_user",
        "password": "test_password",
        "email": "test@gmail.com"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{settings.APP_URL}/auth/register/", json=payload) as response:
            return response


