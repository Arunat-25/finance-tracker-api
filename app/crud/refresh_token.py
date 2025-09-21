from select import select

from app.db.session import session_factory
from app.models.refresh_token import RefreshTokenOrm
from app.models.user import UserOrm
from app.schemas.refresh_token import RefreshTokenCreate


async def add_refresh_token(refresh_token: RefreshTokenCreate):
    async with session_factory() as session:
        token = RefreshTokenOrm(refresh_token=refresh_token.refresh_token, user_id=refresh_token.user_id)
        session.add(token)
        await session.commit()
