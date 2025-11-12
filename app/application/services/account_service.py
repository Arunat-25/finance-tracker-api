from dtos.account_dto import AccountDTO, AccountCreateDTO, AccountResponseDTO, AccountDeleteDTO, AccountGetDTO
from entities.account import Account
from interfaces.account_interface import AccountRepositoryInterface


class AccountService:
    def __init__(self, account_repo: AccountRepositoryInterface):
        self.account_repo = account_repo


    async def get_account_by_id(self, dto: AccountGetDTO) -> AccountResponseDTO:
        account_entity = self._dto_to_entity(dto)
        received_account_entity = await self.account_repo.get_account_by_id(account_entity)
        received_account = self._entity_to_response_dto(received_account_entity)
        return received_account


    async def delete_account_by_id(self, dto: AccountDeleteDTO) -> AccountResponseDTO:
        account_entity = self._dto_to_entity(dto)
        deleted_account = await self.account_repo.delete_account_by_id(account_entity)
        account_dto = self._entity_to_response_dto(deleted_account)
        return account_dto


    async def create_account(self, dto: AccountCreateDTO) -> AccountResponseDTO:
        account_entity = self._dto_to_entity(dto)
        created_account_entity = await self.account_repo.create_account(account_entity)
        created_account = self._entity_to_response_dto(created_account_entity)
        return created_account


    def _dto_to_entity(self, dto):
        entity = Account(owner_id=dto.user_id)
        if hasattr(dto, "account_id"): entity.account_id = dto.account_id
        if hasattr(dto, "name"): entity.name = dto.name
        if hasattr(dto, "balance"): entity.balance = dto.balance
        if hasattr(dto, "currency"): entity.currency = dto.currency

        return entity


    def _entity_to_response_dto(self, entity: Account) -> AccountResponseDTO:
        dto = AccountResponseDTO(
            account_id=entity.account_id,
            name=entity.name,
            balance=entity.balance,
            currency=entity.currency,
            user_id=entity.owner_id,
            is_deleted=entity.is_deleted,
            deleted_at=entity.deleted_at
        )
        return dto
