from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.common.security import decode_token


bearer_scheme = HTTPBearer()

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
    token = credentials.credentials
    decoded_token = decode_token(token)
    user_id = decoded_token["user_id"]
    return user_id


async def get_current_user_utc_offset(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
    token = credentials.credentials
    decoded_token = decode_token(token)
    utc_offset = decoded_token["utc_offset"]
    return utc_offset


async def get_current_user(user_id: int = Depends(get_current_user_id)):
    from app.infrastructure.db.session import session_factory
    from app.infrastructure.db.models.user import UserOrm

    async with session_factory() as session:
        user = await session.get(UserOrm, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user

