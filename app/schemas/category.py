from pydantic import BaseModel

from app.domain.enums.category_type import CategoryTypeEnum


class Category(BaseModel):
    pass


class CategoryCreate(Category):
    title: str
    category_type: CategoryTypeEnum


class CategoryDelete(Category):
    category_id: int
