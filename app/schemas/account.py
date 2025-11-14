from decimal import Decimal

from pydantic import BaseModel

from app.domain.enums.currency import CurrencyEnum


class Account(BaseModel):
    pass

class AccountCreate(Account):
    name: str
    balance: Decimal = Decimal("0.00")
    currency: CurrencyEnum = CurrencyEnum.RUB

class AccountDelete(Account):
    id: int

class AccountGet(Account):
    name: str

class AccountSchema(Account):
    name: str
    balance: Decimal
    currency: CurrencyEnum
