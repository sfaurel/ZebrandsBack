from collections.abc import Generator

import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies.dependencies import get_db
from app.services.account_service import create_account, get_account_by_email
from app.models.account_models import AccountCreate, Account
from app.utils.security import create_access_token

engine_test = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="session", autouse=True)
def create_test_db() -> Generator[None, None, None]:
    SQLModel.metadata.create_all(engine_test)
    yield
    SQLModel.metadata.drop_all(engine_test)


TEST_ACCOUNT = AccountCreate(
    email="test_email@example.com",
    password="secret123",
    role="anonymous"
)


@pytest.fixture()
def test_account(create_test_db) -> Account:
    with Session(engine_test) as session:
        account = create_account(
            session=session, account_create=TEST_ACCOUNT)
        session.commit()
        session.refresh(account)
        return account


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine_test) as session:
        yield session


@pytest.fixture()
def client(db: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_account_token_headers() -> dict[str, str]:
    access_token = create_access_token(
        subject="admin_account@example.com",
        extra_claims={"role": "admin"}
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


@pytest.fixture()
def normal_account_token_headers() -> dict[str, str]:
    access_token = create_access_token(
        subject="normal_account@example.com",
        extra_claims={"role": "anonymous"}
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
