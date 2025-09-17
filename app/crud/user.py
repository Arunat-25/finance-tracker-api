from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from app.db.session import session_factory
from app.models.user import UserOrm
from app.common.security import hash_password
from app.schemas.user import UserCreate


async def create_user(new_user: UserCreate):
    try:
        async with session_factory() as sess:
            hashed_password = hash_password(new_user.password)
            user = UserOrm(
                name=new_user.name,
                email=new_user.email,
                hashed_password=hashed_password,
                is_verified=False
            )
            sess.add(user)
            await sess.commit()
            await sess.refresh(user)
            return user

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email используется другим аккаунтом"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )