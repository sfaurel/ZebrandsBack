from collections.abc import Generator
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
import jwt

from app.utils.security import SECRET_KEY, ALGORITHM
from app.db.connection import engine
from app.models.account_models import Account
from app.schemas.auth_schemas import TokenPayload
from app.services.account_service import get_account_by_email


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_token_data(token: TokenDep) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


def admin_required(token: TokenDep) -> dict:
    payload = get_current_token_data(token)
    role = payload.get("role")
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="The account doesn't have enough privileges"
        )
    return payload


def get_current_account(session: SessionDep, token: TokenDep) -> Account:
    payload = get_current_token_data(token)
    token_data = TokenPayload(**payload)

    account = get_account_by_email(session=session, email=token_data.sub)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if not account.is_active:
        raise HTTPException(status_code=400, detail="Inactive account")
    return account


CurrentAccount = Annotated[Account, Depends(get_current_account)]