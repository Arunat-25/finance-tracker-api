from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base



class AccountOrm(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True) # проиндексирован, так как удаляется по name
    balance: Mapped[float] = mapped_column(default=0.0)
    currency: Mapped[str] = mapped_column(default='RUB')
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    user: Mapped["UserOrm"] = relationship(back_populates="accounts")

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_account_user_name'),
        CheckConstraint('balance >= 0', name='chk_account_balance_positive'),
    )