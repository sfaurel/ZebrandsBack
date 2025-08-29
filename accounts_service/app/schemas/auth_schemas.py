from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str | None = None
    role: str = "anonymous"
    exp: int | None = None


class Credentials(BaseModel):
    email: EmailStr
    password: str


class Message(BaseModel):
    message: str
