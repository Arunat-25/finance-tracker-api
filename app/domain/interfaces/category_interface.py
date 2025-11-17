from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    async def get_categories(self, user_id: int) -> list[Category]:
        pass


    @abstractmethod
    async def delete_category_by_id(self, category: Category) -> Category:
        pass


    @abstractmethod
    async def create_categories(self, categories: list[Category], user_id: int) -> list[Category]:
        pass


    @abstractmethod
    async def create_category(self, category: Category, user_id: int) -> Category:
        pass