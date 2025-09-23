from fastapi import APIRouter, HTTPException, Depends

from app.common.security import decode_token, check_tokens
from app.crud.account import add_account, remove_account
from app.endpoints.exceptions import NotFoundAccount
from app.schemas.account import AccountCreate, AccountDelete
from app.schemas.tokens import TokensCheck

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/create/")
async def create_account(account: AccountCreate):
    return await add_account(account)



@router.delete("/delete/")
async def delete_account(account: AccountDelete, result_check_tokens = Depends(check_tokens)):
    try:
        return await remove_account(account), result_check_tokens
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))


