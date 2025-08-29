import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class AccountBase(SQLModel):
    email: EmailStr = Field(
        unique=True,
        index=True,
        max_length=255,
        nullable=False
    )
    is_active: bool = True
    role: str = Field(default="anonymous", max_length=20, nullable=False)
    full_name: str | None = Field(default=None, max_length=255)


class AccountCreate(AccountBase):
    password: str = Field(min_length=8, max_length=40)


class AccountUpdate(AccountBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class AccountPublic(AccountBase):
    id: uuid.UUID


class Account(AccountBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)

