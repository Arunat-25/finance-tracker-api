import uvicorn

from fastapi import FastAPI

from app.endpoints.auth import router as auth_router
from app.endpoints.account import router as account_router
from app.endpoints.category import router as category_router
from app.endpoints.transaction import router as transaction_router
from app.endpoints.analytics import router as analytics_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(account_router)
app.include_router(category_router)

app.include_router(transaction_router)
app.include_router(analytics_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000,)


