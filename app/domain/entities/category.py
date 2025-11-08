from app.domain.enums.category_type import CategoryTypeEnum


class Category:
    def __init__(self, name: str, category_type: CategoryTypeEnum):
        self.name = name
        self.category_type = category_type