import datetime
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes]
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    refresh_token: Mapped[Optional["RefreshTokenOrm"]] = relationship("RefreshTokenOrm",
                                                                 back_populates="user",
                                                                 uselist=False,
                                                                 cascade="all, delete")
