import asyncio

import aiohttp, pytest
from sqlalchemy import select, delete

from app.common.config import settings
from app.common.security import hash_password
from app.models.user import UserOrm
from app.schemas.user import UserCreate
from tests.fixtures_user import delete_test_user



@pytest.mark.asyncio
async def test_user_register_when_duplicate_email(client, session):
    assert settings.MODE == "TEST"
    stmt = select(UserOrm).where(UserOrm.email == "test@gmail.com")
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()
    if not user:
        user_orm = UserOrm(name="test_user", hashed_password=hash_password("test_pass"), email="test@gmail.com")
        session.add(user_orm)
        await session.commit()

    payload = {
        "name": "test_user",
        "password": "test_password",
        "email": "test@gmail.com"
    }

    async with client.post(f"{settings.APP_URL}/auth/register/", json=payload) as response:
        assert response.status == 400



@pytest.mark.asyncio
async def test_user_register(client, session):
    assert settings.MODE == "TEST"
    stmt = select(UserOrm).where(UserOrm.email == "test@gmail.com")
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()
    if user:
        await session.delete(user)
        await session.commit()

    payload = {
        "name": "test_user",
        "password": "test_password",
        "email": "test@gmail.com"
    }

    async with client.post(f"{settings.APP_URL}/auth/register/", json=payload) as response:
        data = await response.json()

        assert response.status == 201
        assert data["id"]
        assert data["name"] == "test_user"
        assert data["email"] == "test@gmail.com"
        assert data["created_at"]
        assert "password" not in data

