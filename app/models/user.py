import datetime
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[bytes]
    is_verified: Mapped[bool] = mapped_column(default=False, index=True)
    verification_token: Mapped[str | None] = mapped_column(unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    refresh_token: Mapped[Optional["RefreshTokenOrm"]] = relationship("RefreshTokenOrm",
                                                                 back_populates="user",
                                                                 uselist=False,
                                                                 cascade="all, delete")

    accounts: Mapped[List["AccountOrm"]] = relationship("AccountOrm",
                                                           back_populates="user",
                                                           uselist=True,
                                                           cascade="all, delete")

    categories: Mapped[List["CategoryOrm"]] = relationship("CategoryOrm",
                                                           back_populates="user",
                                                           uselist=True,
                                                           cascade="all, delete")