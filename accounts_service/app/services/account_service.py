
from sqlmodel import Session, select


from app.models.account_models import Account, AccountCreate, AccountUpdate
from app.utils.security import get_password_hash


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


def update_account(
    *,
    session: Session,
    db_account: Account,
    account_in: AccountUpdate
) -> Account:
    account_data = account_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in account_data:
        password = account_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_account.sqlmodel_update(account_data, update=extra_data)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account
