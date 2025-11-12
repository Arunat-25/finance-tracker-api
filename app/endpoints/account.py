from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import DBAPIError

from app.dependencies.account_dependencies import get_account_service
from app.dependencies.auth import get_current_user_id
from app.infrastructure.db.session import session_factory
from app.endpoints.exceptions import NotFoundAccount, AccountAlreadyExists
from app.schemas.account import AccountCreate, AccountDelete
from dtos.account_dto import AccountCreateDTO, AccountDeleteDTO, AccountGetDTO
from services.account_service import AccountService

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/create")
async def create_account(
        data: AccountCreate,
        user_id: int = Depends(get_current_user_id),
        account_service: AccountService = Depends(get_account_service)
):
    try:
        account_dto = AccountCreateDTO(
            name=data.name,
            balance=data.balance,
            currency=data.currency,
            user_id=user_id
        )

        crated_account = await account_service.create_account(account_dto)
        return crated_account
    except AccountAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DBAPIError:
        raise HTTPException(status_code=400, detail="Balance is invalid")



@router.delete("/delete")
async def delete_account(
        account: AccountDelete,
        user_id: int = Depends(get_current_user_id),
        account_service: AccountService = Depends(get_account_service)
):
    try:
        dto = AccountDeleteDTO(
            account_id=account.id,
            user_id=user_id
        )
        deleted_account = await account_service.delete_account_by_id(dto)
        return deleted_account
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/get-account")
async def get_account(
        account_id: int,
        user_id: int = Depends(get_current_user_id),
        account_service: AccountService = Depends(get_account_service)
):
    try:
        dto = AccountGetDTO(account_id=account_id, user_id=user_id)
        received_account = await account_service.get_account_by_id(dto)
        return received_account
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))