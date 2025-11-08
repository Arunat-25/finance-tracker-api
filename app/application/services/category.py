from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.category import CategoryRepositoryInterface
from app.domain.entities.category import Category
from app.domain.enums.category_type import CategoryTypeEnum


class CategoryService:
    def __init__(self, session: AsyncSession, category_repo: CategoryRepositoryInterface):
        self.category_repo = category_repo
        self.session = session

    async def create_default_categories(self, user_id: int):
        default_categories = [
            Category(name="Зарплата", category_type=CategoryTypeEnum.INCOME),
            Category(name="Подарок", category_type=CategoryTypeEnum.INCOME),
            Category(name="Инвестиции", category_type=CategoryTypeEnum.INCOME),
            Category(name="Стипендия", category_type=CategoryTypeEnum.INCOME),

            Category(name="Развлечение", category_type=CategoryTypeEnum.EXPENSE),
            Category(name="Продукты", category_type=CategoryTypeEnum.EXPENSE),
            Category(name="Жилье", category_type=CategoryTypeEnum.EXPENSE),
            Category(name="Транспорт", category_type=CategoryTypeEnum.EXPENSE),

            Category(name="Перевод", category_type=CategoryTypeEnum.TRANSFER),
        ]
        created_categories = await self.category_repo.create_categories(
            categories=default_categories,
            user_id=user_id
        )
        return created_categories