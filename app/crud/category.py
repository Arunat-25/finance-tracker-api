from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import session_factory
from app.endpoints.exceptions import CategoryAlreadyExists, CategoryNotFound
from app.enum.category_type import CategoryEnum
from app.models.category import CategoryOrm
from app.schemas.category import CategoryCreate, CategoryDelete


async def create_category(user_id: int, data: CategoryCreate):
    async with session_factory() as session:
        if await category_is_exists(session=session, user_id=user_id, category_title=data.title):
            raise CategoryAlreadyExists("Категория уже существует")

        category = CategoryOrm(title=data.title, user_id=user_id, category_type=data.category_type)
        session.add(category)
        await session.commit()
        await session.refresh(category)
    return category



async def create_default_categories(user_id: int):
    default_categories = [
        CategoryOrm(title="Зарплата", category_type=CategoryEnum.INCOME, user_id=user_id),
        CategoryOrm(title="Подарок", category_type=CategoryEnum.INCOME, user_id=user_id),
        CategoryOrm(title="Инвестиции", category_type=CategoryEnum.INCOME, user_id=user_id),
        CategoryOrm(title="Стипендия", category_type=CategoryEnum.INCOME, user_id=user_id),

        CategoryOrm(title="Развлечение", category_type=CategoryEnum.EXPENSE, user_id=user_id),
        CategoryOrm(title="Продукты", category_type=CategoryEnum.EXPENSE, user_id=user_id),
        CategoryOrm(title="Жилье", category_type=CategoryEnum.EXPENSE, user_id=user_id),
        CategoryOrm(title="Транспорт", category_type=CategoryEnum.EXPENSE, user_id=user_id),
    ]

    async with session_factory() as session:
        for default_category in default_categories:
            if await category_is_exists(session, default_category.user_id, default_category.title):
                raise CategoryAlreadyExists("Категория уже существует")
            session.add(default_category)
        await session.commit()

    return {"message": "Системные категории созданы"}


async def category_is_exists(session: AsyncSession, user_id: int, category_title: str):
    stmt = select(CategoryOrm.id).where(CategoryOrm.title == category_title, CategoryOrm.user_id == user_id)
    res = await session.execute(stmt)
    category_id = res.scalar_one_or_none()
    if category_id is None:
        return False
    return True


async def remove_category(user_id: int, data: CategoryDelete):
    async with session_factory() as session:
        stmt = select(CategoryOrm).where(CategoryOrm.title == data.title, CategoryOrm.user_id == user_id)
        res = await session.execute(stmt)
        category = res.scalar_one_or_none()

        if category is None:
            raise CategoryNotFound("Такой категории у вас нет")

        await session.delete(category)
        await session.commit()
    return {"message": "Категория удалена"}