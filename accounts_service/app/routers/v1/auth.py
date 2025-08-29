from fastapi import APIRouter, HTTPException
from datetime import timedelta

from app.dependencies.dependencies import SessionDep
from app.schemas.auth_schemas import Token, Credentials
from app.services.auth_service import authenticate

from app.utils.security import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    credentials: Credentials
) -> Token:
    """
    Catalog API login, response with an access token
    """
    user = authenticate(
        session=session,
        email=credentials.email,
        password=credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid credentials")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return Token(
        access_token=create_access_token(
            subject=user.email,
            extra_claims={"role": user.role},
            expires_delta=access_token_expires
        ),
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
