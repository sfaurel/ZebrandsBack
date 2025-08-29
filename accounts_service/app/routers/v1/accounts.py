from typing import Any
from fastapi import APIRouter, Depends, HTTPException

from app.services import account_service
from app.dependencies.dependencies import (
    SessionDep,
    admin_required,
)
from app.models.account_models import (
    AccountCreate,
    AccountPublic,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post(
    path="",
    dependencies=[Depends(admin_required)],
    response_model=AccountPublic
)
def create_account(*, session: SessionDep, account_in: AccountCreate) -> Any:
    """
    Create new account.
    """
    account = account_service.get_account_by_email(
        session=session,
        email=account_in.email,
    )
    if account:
        raise HTTPException(
            status_code=400,
            detail="The account with this email already exists in the system.",
        )

    account = account_service.create_account(
        session=session,
        account_create=account_in
    )
    return account
