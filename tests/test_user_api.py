import asyncio

import aiohttp, pytest
from sqlalchemy import select, delete

from app.common.config import settings
from app.common.security import hash_password
from app.models.user import UserOrm
from app.schemas.user import UserCreate
from tests.session import session_factory
from tests.fixtures_user import delete_test_user



@pytest.mark.asyncio
async def test_user_register_when_duplicate_email(db_session):
    assert settings.MODE == "TEST"
    stmt = select(UserOrm).where(UserOrm.email == "test@gmail.com")
    res = await db_session.execute(stmt)
    user = res.scalar_one_or_none()
    if not user:
        user_orm = UserOrm(name="test_user", hashed_password=hash_password("test_pass"), email="test@gmail.com")
        db_session.add(user_orm)
        await db_session.commit()

    payload = {
        "name": "test_user",
        "password": "test_password",
        "email": "test@gmail.com"
    }
    async with aiohttp.ClientSession() as sess:
        async with sess.post(f"{settings.APP_URL}/auth/register/", json=payload) as response:
            assert response.status == 400


@pytest.mark.asyncio
async def test_user_register(db_session, delete_test_user):
    assert settings.MODE == "TEST"
    stmt = select(UserOrm).where(UserOrm.email == "test@gmail.com")
    res = await db_session.execute(stmt)
    user = res.scalar_one_or_none()
    if user:
        await db_session.delete(user)
        await db_session.commit()

    payload = {
        "name": "test_user",
        "password": "test_password",
        "email": "test@gmail.com"
    }
    async with aiohttp.ClientSession() as sess:
        async with sess.post(f"{settings.APP_URL}/auth/register/", json=payload) as response:
            data = await response.json()

            assert response.status == 201
            assert data["id"]
            assert data["name"] == "test_user"
            assert data["email"] == "test@gmail.com"
            assert data["created_at"]
            assert "password" not in data

