from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    async def create_categories(self, categories: list[Category], user_id: int) -> list[Category]:
        pass