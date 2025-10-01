from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class TransactionOrm(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_type: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)

    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    to_account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    account: Mapped["AccountOrm"] = relationship("AccountOrm",
                                                 foreign_keys="[account_id]",
                                                 back_populates="outgoing_transactions")
    to_account: Mapped[Optional["AccountOrm"]] = relationship("AccountOrm",
                                                    foreign_keys="[to_account_id]",
                                                    back_populates="incoming_transactions")

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category: Mapped["CategoryOrm"] = relationship("CategoryOrm", back_populates="transactions")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="transactions")

    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_amount_transaction_bigger_then_zero"),
    )