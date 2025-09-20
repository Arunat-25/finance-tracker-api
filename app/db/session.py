from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.common.config import settings


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

session_factory = async_sessionmaker(engine)
