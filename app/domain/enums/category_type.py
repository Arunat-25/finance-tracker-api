from enum import Enum


class CategoryTypeEnum(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer" # только для категории Перевод