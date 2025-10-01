from enum import Enum


class CategoryEnum(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"