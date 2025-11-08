from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base_class import Base



class CategoryOrm(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    category_type: Mapped[str] = mapped_column(index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["UserOrm"] = relationship(back_populates="categories")

    transactions: Mapped[List["TransactionOrm"]] = relationship("TransactionOrm", back_populates="category")

    is_deleted: Mapped[bool] = mapped_column(index=True, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

