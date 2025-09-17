from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    name: str
    password: str
    email: EmailStr

class UserSchema(UserBase):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


