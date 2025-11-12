from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db_session
from repositories.account_repo import AccountRepository
from services.account_service import AccountService


async def get_account_service(session: AsyncSession = Depends(get_db_session)) -> AccountService:
    account_repo = AccountRepository(session=session)
    account_service = AccountService(account_repo)
    return account_service