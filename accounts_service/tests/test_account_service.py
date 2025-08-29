from sqlmodel import Session
from fastapi.encoders import jsonable_encoder

from app.services.account_service import (
    create_account,
    get_account_by_email,
    update_account
)
from app.models.account_models import Account, AccountCreate, AccountUpdate
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
        update_account(session=db, db_account=account,
                       account_in=account_in_update)
    account_2 = db.get(Account, account.id)
    assert account_2
    assert account.email == account_2.email
    assert verify_password(new_password, account_2.hashed_password)
    assert account_2.full_name == new_name
