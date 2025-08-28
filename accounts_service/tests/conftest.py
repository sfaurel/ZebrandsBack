from collections.abc import Generator

import pytest
from sqlmodel import Session, SQLModel, create_engine


engine_test = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine_test)
    yield
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine_test) as session:
        yield session
