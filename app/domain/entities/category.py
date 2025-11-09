from datetime import datetime

from app.domain.enums.category_type import CategoryTypeEnum


class Category:
    def __init__(
            self,
            owner_id: int,
            name: str | None = None,
            category_type: CategoryTypeEnum | None = None,
            category_id: None | int = None,
            created_at: datetime | None = None,
            deleted_at: datetime | None = None
    ):
        self.category_id = category_id
        self.name = name
        self.category_type = category_type
        self.owner_id = owner_id
        self.created_at = created_at
        self.deleted_at = deleted_at


    @property
    def is_persisted(self) -> bool:
        return self.category_id is not None