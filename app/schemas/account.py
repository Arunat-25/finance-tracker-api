from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.enum.currency import CurrencyEnum


class Account(BaseModel):
    pass

class AccountCreate(Account):
    name: str
    balance: float = 0
    currency: Optional[CurrencyEnum] = None

class AccountDelete(Account):
    name: str

class AccountGet(Account):
    name: str

class AccountSchema(Account):
    name: str
    balance: float
    currency: CurrencyEnum
