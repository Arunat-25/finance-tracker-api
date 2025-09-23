from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base



class AccountOrm(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    balance: Mapped[float] = mapped_column(default=0.0) # прописать чтобы меньше 0 не могло быть
    currency: Mapped[str] = mapped_column(default='RUB')
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    user: Mapped["UserOrm"] = relationship(back_populates="accounts")