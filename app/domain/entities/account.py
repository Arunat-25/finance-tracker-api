from datetime import datetime
from decimal import Decimal

from app.domain.enums.currency import CurrencyEnum


class Account:
    def __init__(
            self,
            owner_id: int,
            account_id: int | None = None,
            name: str | None = None,
            balance: Decimal | None = None,
            currency: CurrencyEnum | None = None,
            is_deleted: bool | None = None,
            deleted_at: datetime | None = None
    ):
        self.owner_id = owner_id
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.currency = currency
        self.is_deleted = is_deleted
        self.deleted_at = deleted_at
