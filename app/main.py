import uvicorn, asyncio

from fastapi import FastAPI
from uvicorn import Config

from app.db.session import engine
from app.db.base_class import Base
from app.endpoints.auth import router as auth_router
from tests.session import test_engine

app = FastAPI()

app.include_router(auth_router)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await create_tables()
    config = Config(app="main:app", port=8001, reload=True)
    server = uvicorn.Server(config=config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())




