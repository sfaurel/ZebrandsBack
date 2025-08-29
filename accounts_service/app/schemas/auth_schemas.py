from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class Credentials(BaseModel):
    email: EmailStr
    password: str
