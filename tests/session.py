from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncSession

from app.common.config import settings

test_engine = create_async_engine(settings.DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

test_session_factory = async_sessionmaker(bind=test_engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    session = AsyncSession(bind=test_engine)
    try:
        yield session
    finally:
        await session.close()