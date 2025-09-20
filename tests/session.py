from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.common.config import settings


test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)

session_factory = async_sessionmaker(test_engine)

