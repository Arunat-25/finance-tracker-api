from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from fastapi.security import HTTPAuthorizationCredentials

from app.dependencies.auth import bearer_scheme
from app.common.security import create_token, check_verify_token
from app.common.email import send_email
from app.repositories.refresh_token import add_refresh_token, update_refresh_token
from app.repositories.user import create_user, check_user, get_user
from app.infrastructure.db.session import session_factory
from app.endpoints.exceptions import EmailAlreadyExists, PasswordIsIncorrect, NotRegistered, NotFoundToken
from app.schemas.email import EmailReceiveAgain
from app.schemas.refresh_token import RefreshTokenCreate, RefreshTokenUpdate
from app.schemas.user import UserSchema, UserCreate, UserCheck, UserTelegramCreate

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register', response_model=UserSchema, status_code=201) #не отправляю информацию, что было отправлено письмо
async def register(new_user: UserCreate | UserTelegramCreate):
    try:
        async with session_factory() as session:
            user = await create_user(session, new_user)
        # await send_email(user.email, user.verification_token)
        return user
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(user: UserCheck):
    try:
        checked_user = await check_user(user)
        user_dict = checked_user

        # email_is_verified = await is_email_verified(user.email)
        # if not email_is_verified:
        #     raise HTTPException(status_code=400, detail="Email is not verified")

        access_token = create_token(user_dict, token_type="access")
        refresh_token = create_token(user_dict, token_type="refresh")

        # Добавление refresh token в бд
        user_for_add_token_in_db = await get_user(email=user.email)
        refresh_token_for_add_in_db = RefreshTokenCreate(
            refresh_token=refresh_token,
            user_id=user_for_add_token_in_db.id
        )
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


@router.put("/refresh")
async def update_refresh(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    refresh_token = credentials.credentials
    refresh_token_to_change = RefreshTokenUpdate(refresh_token=refresh_token)
    try:
        return await update_refresh_token(refresh_token_to_change)
    except NotFoundToken as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/confirm-email") # подумать post запрос или get
async def confirm_email(token: Annotated[str, Query(...)]):
    try:
        await check_verify_token(token)
        return {"message": "Email подтвержден!"}
    except NotFoundToken as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/receive-new-letter")
async def receive_new_letter(email_model: EmailReceiveAgain):
    user = await get_user(email=email_model.email)
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")
    await send_email(user.email, user.verification_token)

    return {"message": f"Новое письмо отправлено на {user.email}"}


# @router.delete("/delete-user")
# async def delete_user(
#         user_id: Annotated[int, None] = None,
#         email: Annotated[str, None] = None,
# ):
#     async with session_factory() as session:
#         if user_id:
#             await remove_user(session=session, user_id=user_id)
#             return {"message": "User deleted"}
#         elif email:
#             await remove_user(session=session, email=email)
#             return {"message": "User deleted"}