from typing import Any
import uuid
from fastapi import APIRouter, Depends, HTTPException

from app.services import account_service
from app.dependencies.dependencies import (
    SessionDep,
    admin_required,
    CurrentAccount
)
from app.models.account_models import (
    Account,
    AccountCreate,
    AccountPublic,
    AccountUpdate,
)
from app.schemas.auth_schemas import Message

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


@router.patch(
    "/{account_id}",
    dependencies=[Depends(admin_required)],
    response_model=AccountPublic,
)
def update_account(
    *,
    session: SessionDep,
    account_id: uuid.UUID,
    account_in: AccountUpdate,
) -> Any:
    """
    Update existing account.
    """

    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(
            status_code=404,
            detail="The account with this id does not exist in the system",
        )
    if account_in.email:
        existing_account = account_service.get_account_by_email(
            session=session,
            email=account_in.email
        )
        if existing_account and existing_account.id != account_id:
            raise HTTPException(
                status_code=409,
                detail="Account with this email already exists"
            )

    db_account = account_service.update_account(
        session=session,
        db_account=db_account,
        account_in=account_in
    )
    return db_account


@router.delete(
    "/{account_id}",
    dependencies=[Depends(admin_required)],
    response_model=Message
)
def delete_account(
    session: SessionDep, current_account: CurrentAccount, account_id: uuid.UUID
) -> Message:
    """
    Delete an account.
    """
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account == current_account:
        raise HTTPException(
            status_code=403,
            detail="Admin accounts are not allowed to delete themselves"
        )
    account_service.delete_account(account)
    session.commit()
    return Message(message="Account deleted successfully")
