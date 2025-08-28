from sqlmodel import Session

from app.services.account_service import create_account
from app.models.account_models import AccountCreate


def test_create_account(db: Session) -> None:
    email = "new_account@example.com"
    password = "new_password"
    account_in = AccountCreate(email=email, password=password)
    account = create_account(session=db, account_create=account_in)
    assert account.email == email
    assert hasattr(account, "hashed_password")
