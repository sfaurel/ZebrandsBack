from sqlmodel import Session
from fastapi.encoders import jsonable_encoder

from app.services.account_service import create_account, get_account_by_email
from app.models.account_models import AccountCreate


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
