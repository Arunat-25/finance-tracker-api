from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.common.config import settings


test_engine = create_async_engine(settings.DATABASE_URL, echo=False)


async def get_session() -> AsyncSession:
    Session = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session
