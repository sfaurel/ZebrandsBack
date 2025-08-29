from sqlmodel import Session
from fastapi.encoders import jsonable_encoder

from app.services.account_service import (
    create_account,
    get_account_by_email,
    update_account,
    delete_account
)
from app.models.account_models import AccountCreate, AccountUpdate
from app.utils.security import verify_password


def test_create_account(db: Session) -> None:
    email = "new_account@example.com"
    password = "new_password"
    account_in = AccountCreate(email=email, password=password)
    account = create_account(session=db, account_create=account_in)
    assert account.email == email
    assert hasattr(account, "hashed_password")


def test_get_account_by_email(db: Session) -> None:
    email = "account@example.com"
    password = "password"
    account_in = AccountCreate(email=email, password=password)
    account = create_account(session=db, account_create=account_in)
    account_2 = get_account_by_email(email=email, session=db)
    assert account_2
    assert account.email == account_2.email
    assert jsonable_encoder(account) == jsonable_encoder(account_2)


def test_update_account(db: Session) -> None:
    password = "old_password"
    email = "old_email@example.com"
    account_in = AccountCreate(email=email, password=password)
    account = create_account(session=db, account_create=account_in)
    new_password = "new_password"
    new_name = "New Name"
    account_in_update = AccountUpdate(
        password=new_password, full_name=new_name)
    if account.id is not None:
        account_2 = update_account(
            session=db,
            db_account=account,
            account_in=account_in_update
        )
    assert account_2
    assert account.email == account_2.email
    assert verify_password(new_password, account_2.hashed_password)
    assert account_2.full_name == new_name


def test_delete_account(db: Session) -> None:
    password = "to_delete_password"
    email = "to_delte_email@example.com"
    account_in = AccountCreate(email=email, password=password)
    account = create_account(session=db, account_create=account_in)
    if account.id is not None:
        account_2 = delete_account(session=db, db_account=account)
    assert account_2
    assert account.email == account_2.email
    assert account_2.is_active is False
