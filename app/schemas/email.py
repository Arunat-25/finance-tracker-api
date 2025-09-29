from pydantic import BaseModel, EmailStr


class EmailBase(BaseModel):
    pass

class EmailReceiveAgain(EmailBase):
    email: EmailStr