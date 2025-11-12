from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass

from enums.currency import CurrencyEnum


@dataclass
class AccountDTO:
    name: str
    balance: Decimal
    currency: CurrencyEnum
    user_id: int


@dataclass
class AccountCreateDTO(AccountDTO):
    pass


@dataclass
class AccountResponseDTO(AccountDTO):
    account_id: int
    is_deleted: bool
    deleted_at: datetime


@dataclass
class AccountDeleteDTO:
    account_id: int
    user_id: int


@dataclass
class AccountGetDTO:
    account_id: int
    user_id: int