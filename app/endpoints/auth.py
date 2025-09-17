from fastapi import APIRouter

from app.crud.user import create_user
from app.schemas.user import UserSchema, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register/', response_model=UserSchema)
async def register(new_user: UserCreate):
    return await create_user(new_user)
