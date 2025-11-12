from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.account import Account


class AccountRepositoryInterface(ABC):
    @abstractmethod
    async def get_account_by_id(self, account: Account) -> Account:
        pass


    @abstractmethod
    async def delete_account_by_id(self, account: Account) -> Account:
        pass


    @abstractmethod
    async def create_account(self, account: Account) -> Account:
        pass