from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from entities.account import Account
from enums.currency import CurrencyEnum
from app.endpoints.exceptions import AccountAlreadyExists, NotFoundAccount
from interfaces.account_interface import AccountRepositoryInterface
from app.infrastructure.models import AccountOrm


class AccountRepository(AccountRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_account_by_id(self, account: Account) -> Account:
        stmt = select(AccountOrm).where(
            AccountOrm.id == account.account_id,
            AccountOrm.user_id == account.owner_id,
            AccountOrm.is_deleted == False
        )
        result = await self.session.execute(stmt)
        account_orm = result.scalar_one_or_none()

        if not account_orm:
            raise NotFoundAccount("Account not found")

        account_entity = self._orm_to_entity(account_orm)
        return account_entity


    async def delete_account_by_id(self, account: Account) -> Account:
        stmt = select(AccountOrm).where(
            AccountOrm.id == account.account_id,
            AccountOrm.user_id == account.owner_id,
            AccountOrm.is_deleted == False
        )
        result = await self.session.execute(stmt)
        account_orm = result.scalar_one_or_none()

        if not account_orm:
            raise NotFoundAccount("Account not found")

        account_orm.is_deleted = True
        account_orm.deleted_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(account_orm)

        account_entity = self._orm_to_entity(account_orm)
        return account_entity


    async def create_account(self, account: Account) -> Account:
        if await self.account_exists_by_name_and_user(account):
            raise AccountAlreadyExists("Account already exists")

        account_orm = self._entity_to_orm(account)
        self.session.add(account_orm)

        await self.session.commit()
        await self.session.refresh(account_orm)

        account_entity = self._orm_to_entity(account_orm)
        return account_entity


    async def account_exists_by_name_and_user(self, account: Account) -> bool:
        stmt = select(AccountOrm.id).where(
            AccountOrm.name == account.name,
            AccountOrm.user_id == account.owner_id,
            AccountOrm.is_deleted == False
        )
        result = await self.session.execute(stmt)
        is_exist = result.scalar() is not None
        return is_exist


    def _orm_to_entity(self, account: AccountOrm) -> Account:
        entity = Account(
            account_id=account.id,
            name=account.name,
            balance=account.balance,
            currency=CurrencyEnum(account.currency),
            owner_id=account.user_id,
            is_deleted=account.is_deleted,
            deleted_at=account.deleted_at
        )
        return entity


    def _entity_to_orm(self, entity: Account) -> AccountOrm:
        orm = AccountOrm(
            name=entity.name,
            balance=entity.balance,
            currency=entity.currency,
            user_id=entity.owner_id
        )
        return orm