from sqlmodel import Session, create_engine, select, SQLModel

from pydantic_core import MultiHostUrl
from dotenv import load_dotenv
import os

from app.models.account_models import Account, AccountCreate
from app.services.account_service import create_account
load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))
DATABASE_NAME = os.getenv("DATABASE_NAME")
ROOT_EMAIL = os.getenv("ROOT_EMAIL")
ROOT_PASSWORD = os.getenv("ROOT_PASSWORD")

DATABASE_URL = MultiHostUrl.build(
    scheme="postgresql+psycopg",
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    path=DATABASE_NAME,
)

engine = create_engine(str(DATABASE_URL))


def init_db(session: Session) -> None:

    SQLModel.metadata.create_all(engine)

    account = session.exec(
        select(Account).where(Account.email == ROOT_EMAIL)
    ).first()
    if not account:
        account_in = AccountCreate(
            email=ROOT_EMAIL,
            password=ROOT_PASSWORD,
            role="admin",
        )
        account = create_account(
            session=session, account_create=account_in)
