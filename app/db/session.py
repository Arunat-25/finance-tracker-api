from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.common.config import settings
from app.db.base_class import Base
from app.models.user import UserOrm


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

session_factory = async_sessionmaker(engine)
