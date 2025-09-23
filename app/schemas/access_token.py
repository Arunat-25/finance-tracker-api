from pydantic import BaseModel


class AccessTokenBase(BaseModel):
    pass


class AccessTokenCheck(AccessTokenBase):
    token: str
    token_type: str