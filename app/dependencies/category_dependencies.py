from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.category_service import CategoryService
from app.infrastructure.db.session import get_db_session
from app.infrastructure.repositories.category_repo import CategoryRepository


async def get_category_service(session: AsyncSession = Depends(get_db_session)) -> CategoryService:
    category_repo = CategoryRepository(session=session)
    return CategoryService(category_repo=category_repo)