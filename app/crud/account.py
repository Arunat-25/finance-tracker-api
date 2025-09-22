from sqlalchemy import delete

from app.db.session import session_factory
from app.endpoints.exceptions import NotFoundAccount
from app.models.account import AccountOrm
from app.schemas.account import AccountCreate, AccountDelete


async def add_account(account: AccountCreate):
    async with session_factory() as session:
        account_to_add = AccountOrm(
            name=account.name,
            balance=account.balance,
            currency=account.currency,
            user_id=account.user_id,
        )
        session.add(account_to_add)
        await session.commit()
        await session.refresh(account_to_add)

    return {
        "id": account.id,
        "name": account_to_add.name,
        "balance": account_to_add.balance,
        "currency": account_to_add.currency,
        "user_id": account_to_add.user_id,
    }


async def remove_account(account: AccountDelete):
    async with session_factory() as session:
        stmt = delete(AccountOrm).where(AccountOrm.id == account.id)
        res = await session.execute(stmt)
        await session.commit()
    if res.rowcount:
        return {"Success": True}
    raise NotFoundAccount("Account not found")
