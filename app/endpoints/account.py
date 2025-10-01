from fastapi import APIRouter, HTTPException, Depends

from app.auth_dependencies import get_current_user, get_current_user_id
from app.common.security import decode_token
from app.crud.account import add_account, remove_account, get_account
from app.endpoints.exceptions import NotFoundAccount, AccountAlreadyExists
from app.schemas.account import AccountCreate, AccountDelete, AccountGet, AccountSchema
from app.schemas.access_token import AccessTokenCheck

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/create")
async def create_account(account: AccountCreate, user_id: int = Depends(get_current_user_id)):
    try:
        return await add_account(account,user_id)
    except AccountAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.delete("/delete")
async def delete_account(account: AccountDelete, user_id: int = Depends(get_current_user_id)):
    try:
        return await remove_account(account, user_id)
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/get-account")
async def get_account_detail(account_name: str, user_id: int = Depends(get_current_user_id)):
    try:
        account = await get_account(account_name, user_id)
        return account
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))