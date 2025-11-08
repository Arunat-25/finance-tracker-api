from fastapi import HTTPException
from sqlalchemy import select

from app.infrastructure.db.session import session_factory
from app.infrastructure.models.user import UserOrm


async def is_email_verified(email: str):
    async with session_factory() as session:
        stmt = select(UserOrm.is_verified).where(UserOrm.email == email)
        result = await session.execute(stmt)
        is_verified = result.scalar()
        if is_verified is None:
            raise HTTPException(status_code=404, detail="Email not found")
    return is_verified