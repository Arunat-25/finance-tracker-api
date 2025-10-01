from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base



class AccountOrm(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True) # проиндексирован, так как удаляется по name
    balance: Mapped[float] = mapped_column(default=0.0, nullable=False)
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
    deleted_at: Mapped[datetime | None] = mapped_column(default=None, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_account_user_name'),
        CheckConstraint('balance >= 0', name='chk_account_balance_positive'),
    )