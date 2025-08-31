from collections.abc import Generator

import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies.dependencies import get_db
from app.utils.security import create_access_token
from app.models.product_models import Product

engine_test = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="session", autouse=True)
def create_test_db() -> Generator[None, None, None]:
    SQLModel.metadata.create_all(engine_test)
    yield
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture(scope="session", autouse=True)
def db(create_test_db) -> Generator[Session, None, None]:
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
        subject="normal_account@example.com",
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
