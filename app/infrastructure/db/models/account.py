from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, CheckConstraint, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base_class import Base
from decimal import Decimal


class AccountOrm(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True) # проиндексирован, так как удаляется по name
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"), nullable=False)
    currency: Mapped[str] = mapped_column(default="RUB", nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user: Mapped["UserOrm"] = relationship(back_populates="accounts")

    outgoing_transactions: Mapped[List["TransactionOrm"]] = relationship("TransactionOrm",
                                                                         back_populates="account",
                                                                         foreign_keys="[TransactionOrm.account_id]")
    incoming_transactions: Mapped[List["TransactionOrm"]] = relationship("TransactionOrm",
                                                                         back_populates="to_account",
                                                                         foreign_keys="[TransactionOrm.to_account_id]")

    is_deleted: Mapped[bool] = mapped_column(default=False, index=True, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    __table_args__ = (
        CheckConstraint('balance >= 0', name='chk_account_balance_positive'),
    )