from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator
from decimal import Decimal

from enums.transaction_type import TransactionEnum


class Transaction(BaseModel):
    pass


class TransferCreate(Transaction):
    account_id: int
    to_account_id: int
    amount: Decimal
    commission: Decimal = Decimal("0.00")
    rate: Decimal | None = None
    category_id: int


class TransactionIncomeCreate(Transaction):
    account_id: int
    amount: Decimal
    category_id: int


class TransactionExpenseCreate(Transaction):
    account_id: int
    amount: Decimal
    category_id: int


class TransactionsGet(Transaction):
    list_account_id: Optional[list[int]] = None
    list_category_id: Optional[list[int]] = None
    list_transaction_type: Optional[list[TransactionEnum]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = Field(default=50, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


    @model_validator(mode="after")
    def validate_data(self):
        if self.date_to and self.date_from:
            if self.date_to < self.date_from:
                raise ValueError("data_to не может быть раньше data_from")
            return self
        return self