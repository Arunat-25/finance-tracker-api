from datetime import datetime, timezone, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.account import account_is_exists, get_account
from app.crud.category import category_exists
from app.currency import get_rates
from app.db.session import session_factory
from app.endpoints.exceptions import NotEnoughMoney, NotFoundAccount, CategoryNotFound
from app.enum.transaction_type import TransactionEnum
from app.models import TransactionOrm, AccountOrm
from app.schemas.transaction import TransferCreate, TransactionIncomeCreate, TransactionExpenseCreate, TransactionsGet, \
    Transaction


async def create_expense(data: TransactionExpenseCreate, user_id: int):
    async with session_factory() as session:
        if not category_exists(session=session, user_id=user_id, category_id=data.category_id):
            raise CategoryNotFound

        account = await get_account(session=session, account_id=data.account_id, user_id=user_id)
        account.balance = account.balance - data.amount

        transaction = TransactionOrm(
            transaction_type=TransactionEnum.EXPENSE,
            amount=data.amount,
            date=datetime.utcnow(),
            account_id=data.account_id,
            to_account_id=None,
            rate=None,
            commission=None,
            category_id=data.category_id,
            user_id=user_id,
            balance_after=account.balance,
        )
        session.add(transaction)

        await session.commit()
        await session.refresh(account)
        await session.refresh(transaction)

        return account, transaction


async def create_income(data: TransactionIncomeCreate, user_id: int):
    async with session_factory() as session:
        if not await category_exists(session=session, user_id=user_id, category_id=data.category_id):
            raise CategoryNotFound

        account = await get_account(session=session, account_id=data.account_id, user_id=user_id)
        account.balance = account.balance + data.amount

        transaction = TransactionOrm(
            transaction_type=TransactionEnum.INCOME,
            amount=data.amount,
            date=datetime.now(timezone.utc),
            account_id=data.account_id,
            to_account_id=None,
            rate=None,
            commission=None,
            category_id=data.category_id,
            user_id=user_id,
            balance_after=account.balance,
        )
        session.add(transaction)

        await session.commit()
        await session.refresh(transaction)
        await session.refresh(account)

        return account, transaction


async def create_transfer(data: TransferCreate, user_id: int):
    async with session_factory() as session:
        if not await category_exists(session=session, user_id=user_id, category_id=data.category_id):
            raise CategoryNotFound

        account, to_account = await withdraw_and_deposit_money(
            session=session,
            account_id=data.account_id,
            to_account_id=data.to_account_id,
            user_id=user_id,
            amount=data.amount,
            commission=data.commission,
            rate=data.rate,
        )

        transfer = TransactionOrm(
            transaction_type=TransactionEnum.TRANSFER,
            amount=data.amount,
            date=datetime.now(timezone.utc),
            account_id=data.account_id,
            to_account_id=data.to_account_id,
            category_id=data.category_id,
            user_id=user_id,
            rate=data.rate,
            commission=data.commission,
            balance_after=account.balance,
        )
        session.add(transfer)

        income_transfer = TransactionOrm(
            transaction_type=TransactionEnum.TRANSFER,
            amount=data.amount,
            date=datetime.now(timezone.utc),
            account_id=data.to_account_id,
            to_account_id=None,
            category_id=data.category_id,
            user_id=user_id,
            rate=None,
            commission=None,
            balance_after=to_account.balance,
        )
        session.add(income_transfer)

        await session.commit()
        await session.refresh(income_transfer)
        await session.refresh(transfer)

        return income_transfer, transfer


async def withdraw_and_deposit_money(
        session: AsyncSession,
        account_id: int,
        to_account_id: int,
        user_id: int,
        amount: Decimal,
        commission: Decimal,
        rate: Decimal | None
):
    stmt = select(AccountOrm).where(
        AccountOrm.id.in_([account_id, to_account_id]), AccountOrm.user_id == user_id
    ).with_for_update()
    res = await session.execute(stmt)
    accounts_map = {acc.id: acc for acc in res.scalars()}

    if len(accounts_map) != 2:
        raise NotFoundAccount("Счет не найден!")

    account = accounts_map[account_id]
    to_account = accounts_map[to_account_id]

    if amount + commission > account.balance:
        raise NotEnoughMoney("Недостаточно средств!")

    if rate is None:
        rates = await get_rates(base_currency=account.currency)
        to_account_rate_value = rates[to_account.currency]
    else:
        to_account_rate_value = rate

    account.balance =  account.balance - amount - commission
    to_account.balance = to_account.balance + amount*Decimal(to_account_rate_value)

    return account, to_account


async def get_transactions(data: TransactionsGet, user_id: int):
    async with session_factory() as session:
        conditions = [TransactionOrm.user_id == user_id]

        if data.list_account_id:
            conditions.append(TransactionOrm.account_id.in_(data.list_account_id))
        if data.list_category_id:
            conditions.append(TransactionOrm.category_id.in_(data.list_category_id))
        if data.list_transaction_type:
            conditions.append(TransactionOrm.transaction_type.in_(data.list_transaction_type))
        if data.date_from:
            conditions.append(TransactionOrm.date >= data.date_from)
        if data.date_to:
            conditions.append(TransactionOrm.date < data.date_to + timedelta(days=1))

        stmt = select(TransactionOrm
                      ).where(*conditions
                              ).order_by(TransactionOrm.id.desc()
                                         ).limit(data.limit
                                                 ).offset(data.offset)
        res = await session.execute(stmt)
        transactions = res.scalars().all()
        return transactions


