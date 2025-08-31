from collections.abc import Generator
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
import jwt

from app.utils.security import SECRET_KEY, ALGORITHM
from app.db.connection import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

bearer_scheme = HTTPBearer()


TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]


def get_current_token_data(token: TokenDep) -> dict:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY,
                             algorithms=[ALGORITHM])
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
