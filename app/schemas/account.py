from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    pass


class CurrencyEnum(str, Enum):
    RUB = 'RUB' # Рубль
    INR = 'INR' # Индийская рупия
    IRR = 'IRR' # Иранский риал
    BRL = 'BRL' # Бразильский реал
    UZC = 'UZC' # Узбекский сум
    TRY = 'TRY' # Турецкая лира
    BYN = 'BYN' # Белорусский рубль
    KZT = 'KZT' # Тенге
    UAH = 'UAH' # Гривна
    USD = 'USD' # Доллар
    EUR = 'EUR' # Евро
    JPY = 'JPY' # Иена
    GBP = 'GBP' # Фунт Стерлингов
    CNY = 'CNY' # Юань


class AccountCreate(Account):
    name: str
    balance: float = 0
    currency: Optional[CurrencyEnum] = None


class AccountDelete(Account):
    name: str