from pydantic import BaseModel


class TokensBase(BaseModel):
    pass


class TokensCheck(TokensBase):
    access_token: str
    token_type: str
    refresh_token: str