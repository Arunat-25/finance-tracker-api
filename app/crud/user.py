from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import session_factory
from app.endpoints.exceptions import EmailAlreadyExists, PasswordIsIncorrect, NotRegistered
from app.models.user import UserOrm
from app.common.security import hash_password, check_password, create_verify_token
from app.schemas.user import UserCreate, UserCheck


async def create_user(session: AsyncSession, new_user: UserCreate):
    try:
        hashed_password = hash_password(new_user.password)
        user = UserOrm(
            name=new_user.name,
            email=new_user.email,
            hashed_password=hashed_password,
            is_verified=False,
            verification_token=create_verify_token(),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    except IntegrityError:
         raise EmailAlreadyExists("Email уже зарегистрирован") # изменить обработку, так как не только когда email
                                                               # существует срабатывает IntegrityError
    except Exception:
         raise HTTPException(
             status_code=500,
             detail=f"Ошибка при создании пользователя"
         )


async def check_user(user: UserCheck):
    try:
        async with session_factory() as sess:
            stmt = select(UserOrm).where(UserOrm.email == user.email)
            res = await sess.execute(stmt)
            db_user = res.scalar_one_or_none()
            if db_user:
                if check_password(user.password, db_user.hashed_password):
                    return {
                        "user_id": db_user.id,
                        "name": db_user.name,
                        "email": db_user.email,
                    }
                raise PasswordIsIncorrect("Неправильный пароль")
            raise NotRegistered("Пользователь не зарегистрирован")

    except (PasswordIsIncorrect, NotRegistered):
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при входе"
        )


async def get_user(user_id: int = None, email: str = None):
    async with session_factory() as sess:
        if user_id:
            stmt = select(UserOrm).where(UserOrm.id == user_id)
        elif email:
            stmt = select(UserOrm).where(UserOrm.email == email)

        res = await sess.execute(stmt)
        db_user = res.scalar_one_or_none()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
    return db_user



async def remove_user(session: AsyncSession, user_id: int = None, email: str = None):
    if user_id:
        user = await get_user(user_id=user_id)
        await session.delete(user)
        await session.commit()
    elif email:
        user = await get_user(email=email)
        await session.delete(user)
        await session.commit()











