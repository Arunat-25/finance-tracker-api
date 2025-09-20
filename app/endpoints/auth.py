from fastapi import APIRouter, HTTPException

from app.crud.user import create_user, check_user
from app.db.session import session_factory
from app.endpoints.exceptions import EmailAlreadyExists, PasswordIsIncorrect, NotRegistered
from app.schemas.user import UserSchema, UserCreate, UserCheck

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
        return await check_user(user)
    except PasswordIsIncorrect as e:
        raise HTTPException(status_code=401, detail=str(e))
    except NotRegistered as e:
        raise HTTPException(status_code=404, detail=str(e))