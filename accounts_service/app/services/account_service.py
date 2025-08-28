
from sqlmodel import Session

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
