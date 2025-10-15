from datetime import datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy import ForeignKey, CheckConstraint, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class TransactionOrm(Base):
    """Поля to_account_id, rate и commission не None только при transaction_type = transfer(Перевод со счета на счет)"""
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_type: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False) # вынести 12 и 2 в переменнве окружения
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False) # индекс поставить

    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    to_account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    account: Mapped["AccountOrm"] = relationship("AccountOrm",
                                                 foreign_keys=[account_id],
                                                 back_populates="outgoing_transactions")
    to_account: Mapped[Optional["AccountOrm"]] = relationship("AccountOrm",
                                                    foreign_keys=[to_account_id],
                                                    back_populates="incoming_transactions")
    rate: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), default=None)
    commission: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), default=None)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category: Mapped["CategoryOrm"] = relationship("CategoryOrm", back_populates="transactions")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="transactions")

    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_amount_transaction_bigger_then_zero"),
    )