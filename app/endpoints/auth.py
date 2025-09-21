from fastapi import APIRouter, HTTPException, Response
from select import select

from app.common.security import create_token
from app.crud.refresh_token import add_refresh_token, update_refresh_token
from app.crud.user import create_user, check_user, get_user
from app.db.session import session_factory
from app.endpoints.exceptions import EmailAlreadyExists, PasswordIsIncorrect, NotRegistered, NotFoundToken
from app.models.refresh_token import RefreshTokenOrm
from app.schemas.refresh_token import RefreshTokenCreate, RefreshTokenUpdate
from app.schemas.user import UserSchema, UserCreate, UserCheck
from tests import session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register/', response_model=UserSchema, status_code=201)
async def register(new_user: UserCreate):
    try:
        async with session_factory() as session:
            return await create_user(session, new_user)
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/authenticate/")
async def login(user: UserCheck):
    try:
        await check_user(user)
        user_dict = {"email": user.email}
        access_token = create_token(user_dict, token_type="access")
        refresh_token = create_token(user_dict, token_type="refresh")

        # Добавление refresh token в бд
        user_for_add_token_in_db = await get_user(email=user.email)
        refresh_token_for_add_in_db = RefreshTokenCreate(refresh_token=refresh_token, user_id=user_for_add_token_in_db.id)
        await add_refresh_token(refresh_token_for_add_in_db)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token
        }

    except PasswordIsIncorrect as e:
        raise HTTPException(status_code=401, detail=str(e))
    except NotRegistered as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/refresh/")
async def update_refresh(refresh_token: RefreshTokenUpdate):
    try:
        return await update_refresh_token(refresh_token)
    except NotFoundToken as e:
        raise HTTPException(status_code=404, detail=str(e))