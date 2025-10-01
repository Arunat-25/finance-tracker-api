from pydantic import BaseModel

from app.enum.category_type import CategoryEnum


class Category(BaseModel):
    pass


class CategoryCreate(Category):
    title: str
    category_type: CategoryEnum


class CategoryDelete(Category):
    title: str
