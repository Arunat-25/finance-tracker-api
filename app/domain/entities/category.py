from datetime import datetime

from app.domain.enums.category_type import CategoryTypeEnum
from app.domain.exceptions.categories import CategoryNameTooShort, CategoryNameTooLong


class Category:
    def __init__(
            self,
            owner_id: int,
            name: str,
            category_type: CategoryTypeEnum,
            created_at: datetime,
            category_id: None | int = None,
            deleted_at: datetime | None = None
    ):
        self.category_id = category_id
        self.name = self._validate_name(name)
        self.category_type = category_type
        self.owner_id = owner_id
        self.created_at = created_at
        self.deleted_at = deleted_at


    def _validate_name(self, name: str) -> str:
        if len(name.split()) == 0:
            raise CategoryNameTooShort(name)
        elif len(name) > 20:
            raise CategoryNameTooLong(name)
        return name