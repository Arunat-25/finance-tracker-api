from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.category_type import CategoryTypeEnum


@dataclass
class CategoryDTO:
    name: str
    category_type: CategoryTypeEnum
    user_id: int


@dataclass
class CategoryCreateDTO(CategoryDTO):
    pass


@dataclass
class CategoryResponseDTO(CategoryDTO):
    category_id: int
    created_at: datetime
    deleted_at: datetime | None