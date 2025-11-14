from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db_session
from app.infrastructure.repositories.account_repo import AccountRepository
from app.application.services.account_service import AccountService


async def get_account_service(session: AsyncSession = Depends(get_db_session)) -> AccountService:
    account_repo = AccountRepository(session=session)
    account_service = AccountService(account_repo)
    return account_service