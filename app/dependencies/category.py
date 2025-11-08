from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.category import CategoryService
from app.infrastructure.db.session import get_db_session
from app.infrastructure.repositories.category import CategoryRepository


async def get_category_service(session: AsyncSession = Depends(get_db_session)) -> CategoryService:
    category_repo = CategoryRepository(session=session)
    return CategoryService(session=session, category_repo=category_repo)