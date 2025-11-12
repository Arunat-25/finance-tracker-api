from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.endpoints.exceptions import NotFoundAccount
from app.infrastructure.models import AccountOrm
from app.schemas.account import AccountCreate, AccountDelete


async def get_account(session: AsyncSession, account_id: int, user_id: int):
    stmt = select(AccountOrm).where(
        AccountOrm.id == account_id,
        AccountOrm.user_id == user_id,
        AccountOrm.is_deleted == False
    )
    res = await session.execute(stmt)
    account = res.scalar_one_or_none()

    if account is None:
        raise NotFoundAccount("Account not found")

    return account


async def get_accounts(session: AsyncSession, user_id: int, account_ids: list[int]):
    stmt = select(AccountOrm).where(
        AccountOrm.user_id == user_id,
        AccountOrm.is_deleted == False,
        AccountOrm.id.in_(account_ids)
    )
    res = await session.execute(stmt)
    accounts = res.scalars().all()

    return accounts