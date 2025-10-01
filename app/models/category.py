from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base



class CategoryOrm(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    category_type: Mapped[str] = mapped_column(index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["UserOrm"] = relationship(back_populates="categories")

    __table_args__ = (
        UniqueConstraint('user_id', 'title', name='uq_user_category_title'),
    )