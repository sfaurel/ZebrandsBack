from sqlmodel import Session

from app.models.account_models import Account
from app.services.account_service import get_account_by_email
from app.utils.security import verify_password


def authenticate(
    *,
    session: Session,
    email: str,
    password: str
) -> Account | None:
    db_account = get_account_by_email(session=session, email=email)
    if not db_account:
        return None
    if not verify_password(password, db_account.hashed_password):
        return None
    return db_account
