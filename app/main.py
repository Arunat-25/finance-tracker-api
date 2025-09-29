import uvicorn, asyncio

from fastapi import FastAPI
from uvicorn import Config

from app.db.session import engine
from app.db.base_class import Base
from app.endpoints.auth import router as auth_router
from app.endpoints.account import router as account_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(account_router)



async def main():
    config = Config(app="main:app", port=8001, reload=True)
    server = uvicorn.Server(config=config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())




