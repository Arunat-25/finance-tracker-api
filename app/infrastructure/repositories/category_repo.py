from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.interfaces.category import CategoryRepositoryInterface
from app.domain.entities.category import Category
from app.domain.enums.category_type import CategoryTypeEnum
from app.endpoints.exceptions import CategoryAlreadyExists
from app.infrastructure.models import CategoryOrm


class CategoryRepository(CategoryRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_category(self, category: Category, user_id: int) -> Category:
        if await self.category_exists_by_name_and_user(category, user_id):
           raise CategoryAlreadyExists("Category already exists")
        category_orm = self._entity_to_orm(category, user_id)
        self.session.add(category_orm)
        await self.session.commit()
        await self.session.refresh(category_orm)

        created_category = self._orm_to_entity(category_orm)
        return created_category


    async def create_categories(self, categories: list[Category], user_id: int) -> list[Category]:
        category_existence = await self.categories_exist_by_name_and_user(categories, user_id)
        created_categories = []
        for category in categories:
            if not category_existence[category.name]:
                created_categories.append(category)
                category_orm = self._entity_to_orm(category, user_id)
                self.session.add(category_orm)
        await self.session.commit()
        return created_categories


    def _entity_to_orm(self, entity: Category, user_id: int) -> CategoryOrm:
        category_orm = CategoryOrm(
            title=entity.name,
            category_type=entity.category_type,
            user_id=user_id
        )
        return category_orm


    def _orm_to_entity(self, orm: CategoryOrm) -> Category:
        entity = Category(
            category_id=orm.id,
            name=orm.title,
            category_type=CategoryTypeEnum(orm.category_type),
            owner_id=orm.user_id,
            created_at=orm.created_at,
            deleted_at=orm.deleted_at
        )
        return entity


    async def category_exists_by_name_and_user(self, category: Category, user_id: int) -> bool:
        stmt = select(CategoryOrm.id).where(
            CategoryOrm.title == category.name,
            CategoryOrm.user_id == user_id,
            CategoryOrm.is_deleted == False
        )
        result = await self.session.execute(stmt)
        is_exists = result.scalar() is not None
        return is_exists


    async def categories_exist_by_name_and_user(self, categories: list[Category], user_id: int) -> dict[str, bool]:
        category_names = [category.name for category in categories]
        stmt = select(CategoryOrm.title).where(
            CategoryOrm.title.in_(category_names),
            CategoryOrm.user_id == user_id,
            CategoryOrm.is_deleted == False
        )
        result = await self.session.execute(stmt)
        categories_name_in_db = set(result.scalars().all())

        category_existence = {category.name: category.name in categories_name_in_db for category in categories}
        return category_existence
