from pycparser.ply.yacc import token
from sqlalchemy import select, exists
from sqlalchemy.orm import joinedload

from app.common.security import create_token, decode_token
from app.crud.user import get_user
from app.db.session import session_factory
from app.endpoints.exceptions import NotFoundToken
from app.models.refresh_token import RefreshTokenOrm
from app.models.user import UserOrm
from app.schemas.refresh_token import RefreshTokenCreate, RefreshTokenUpdate


async def add_refresh_token(refresh_token: RefreshTokenCreate):
    async with session_factory() as session:
        stmt = select(RefreshTokenOrm).where(RefreshTokenOrm.user_id == refresh_token.user_id)
        res = await session.execute(stmt)
        token_exists = res.scalar_one_or_none()
        if token_exists:
            await session.delete(token_exists)
            await session.commit()

        token_to_db = RefreshTokenOrm(refresh_token=refresh_token.refresh_token, user_id=refresh_token.user_id)
        session.add(token_to_db)
        await session.commit()


async def update_refresh_token(refresh_token: RefreshTokenUpdate):
    decoded_token = decode_token(refresh_token.refresh_token)
    async with session_factory() as session:
        stmt = select(RefreshTokenOrm).options(joinedload(RefreshTokenOrm.user)).where(
            RefreshTokenOrm.user_id == decoded_token["user_id"]
        )
        res = await session.execute(stmt)
        db_refresh_token = res.scalar_one_or_none()
        if not db_refresh_token or db_refresh_token.refresh_token != refresh_token.refresh_token:
            raise NotFoundToken("Токена в БД нет")

        new_refresh_token = create_token({"email": db_refresh_token.user.email}, "refresh")
        new_access_token = create_token({"email": db_refresh_token.user.email}, "access")

        db_refresh_token.refresh_token = new_refresh_token
        await session.commit()
        await session.refresh(db_refresh_token)

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "refresh_token": db_refresh_token.refresh_token,
        "user_id": db_refresh_token.user.id
    }
