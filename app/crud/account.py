from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import session_factory
from app.endpoints.exceptions import NotFoundAccount, AccountAlreadyExists
from app.models.account import AccountOrm
from app.schemas.account import AccountCreate, AccountDelete, AccountGet, Account


async def add_account(account: AccountCreate, user_id: int):
    async with session_factory() as session:
        if await account_is_exists(session=session, user_id=user_id, account_name=account.name):
            raise AccountAlreadyExists("Счет с таким названием уже существует")

        account_to_add = AccountOrm(
            name=account.name,
            balance=account.balance,
            currency=account.currency,
            user_id=user_id,
        )
        session.add(account_to_add)
        await session.commit()
        await session.refresh(account_to_add)

    return {
        "id": account_to_add.id,
        "name": account_to_add.name,
        "balance": account_to_add.balance,
        "currency": account_to_add.currency,
        "user_id": account_to_add.user_id,
    }


async def account_is_exists(session: AsyncSession, user_id: int, account_name: str):
    stmt = select(AccountOrm.id).where(
        AccountOrm.user_id == user_id,
                    AccountOrm.name == account_name,
                    AccountOrm.is_deleted == False
    )
    res = await session.execute(stmt)
    account_id = res.scalar_one_or_none()
    if account_id is None:
        return False
    return True


async def remove_account(data: AccountDelete, user_id: int):
    async with session_factory() as session:
        stmt = select(AccountOrm).where(
            AccountOrm.name == data.name,
            AccountOrm.user_id == user_id,
            AccountOrm.is_deleted == False
        )
        res = await session.execute(stmt)
        account = res.scalar_one_or_none()

        if account is None:
            raise NotFoundAccount("Account not found")

        account.is_deleted = True
        account.deleted_at = datetime.now(timezone.utc)
        await session.commit()
    return {"message": "Счет удален"}


async def get_account(session: AsyncSession, account_id: int, user_id: int):
    stmt = select(AccountOrm).where(
        AccountOrm.id == account_id,
        AccountOrm.user_id == user_id,
        AccountOrm.is_deleted == False
    ).with_for_update()
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