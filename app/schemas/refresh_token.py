from pydantic import BaseModel


class RefreshTokenBase(BaseModel):
    pass


class RefreshTokenCreate(RefreshTokenBase):
    refresh_token: str
    user_id: int


class RefreshTokenUpdate(RefreshTokenBase):
    refresh_token: str
