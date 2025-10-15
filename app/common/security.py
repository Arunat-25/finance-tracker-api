from datetime import timezone, datetime, timedelta
import bcrypt, secrets
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from fastapi import HTTPException
from sqlalchemy import select

from app.db.session import session_factory
from app.endpoints.exceptions import NotFoundToken
from app.models.user import UserOrm


def hash_password(password: str) -> bytes:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def create_token(data: dict, token_type: str) -> str:
    with open("C:/Users/aruna/Desktop/finance-tracker-api/app/common/private.pem", "rb") as file_key:
        private_key = file_key.read()
    exp = None
    if token_type == "access":
        exp = datetime.now(timezone.utc) + timedelta(minutes=2)
    elif token_type == "refresh":
        exp = datetime.now(timezone.utc) + timedelta(minutes=60)
    data['exp'] = exp
    token = jwt.encode(data, private_key, algorithm="RS256")
    return token


def decode_token(token: str) -> dict:
    try:
        with open("C:/Users/aruna/Desktop/finance-tracker-api/app/common/public.pem", "rb") as file_key:
            public_key = file_key.read()
        return jwt.decode(token, public_key, algorithms=["RS256"])

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Public key not found"
        )


def create_verify_token():
    return secrets.token_urlsafe(32)


async def check_verify_token(token: str):
    async with session_factory() as session:
        stmt = select(UserOrm).where(UserOrm.verification_token == token)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()

        if not user:
            raise NotFoundToken("Token not found")

        user.verification_token = None
        user.is_verified = True
        await session.commit()
        await session.refresh(user)

        return user
        # возвращать не user, а пару токенов

