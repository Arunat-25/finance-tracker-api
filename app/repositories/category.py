from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.models import CategoryOrm




async def category_exists(session: AsyncSession, user_id: int, category_id: int):
    stmt = select(CategoryOrm.id).where(
        CategoryOrm.id == category_id,
        CategoryOrm.user_id == user_id,
        CategoryOrm.is_deleted == False,
    )
    res = await session.execute(stmt)
    category_id = res.scalar_one_or_none()
    if category_id is None:
        return False
    return True