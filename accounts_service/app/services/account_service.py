
from sqlmodel import Session, select


from app.models.account_models import Account, AccountCreate
from app.services.auth_service import get_password_hash


def create_account(
    *,
    session: Session,
    account_create: AccountCreate
) -> Account:

    db_obj = Account.model_validate(
        account_create, update={
            "hashed_password": get_password_hash(account_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_account_by_email(*, session: Session, email: str) -> Account | None:
    statement = select(Account).where(Account.email == email)
    session_account = session.exec(statement).first()
    return session_account
