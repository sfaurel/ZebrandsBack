from fastapi.testclient import TestClient
from sqlmodel import Session

from app.services.account_service import create_account, get_account_by_email
from app.models.account_models import AccountCreate


def test_create_account_existing_email(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
    db: Session
) -> None:
    email = "repeated_email@example.com"
    password = "password"
    account_in = AccountCreate(email=email, password=password)
    create_account(session=db, account_create=account_in)
    data = {"email": email, "password": password}
    response = client.post(
        "/api/v1/accounts",
        headers=admin_account_token_headers,
        json=data,
    )
    created_account = response.json()
    assert response.status_code == 400
    assert "_id" not in created_account

#TODO: check why this test make someothers tests fail
# def test_create_account_new_email(
#     client: TestClient,
#     admin_account_token_headers: dict[str, str],
#     db: Session
# ) -> None:
#     email = "new_email@example.com"
#     password = "password"
#     data = {"email": email, "password": password}
#     response = client.post(
#         "/api/v1/accounts",
#         headers=admin_account_token_headers,
#         json=data,
#     )
#     assert 200 <= response.status_code < 300
#     created_account = response.json()
#     account = get_account_by_email(session=db, email=email)
#     assert account
#     assert account.email == created_account["email"]


def test_create_account_by_normal_user(
    client: TestClient,
    normal_account_token_headers: dict[str, str]
) -> None:
    email = "from_normal_account@example.com"
    password = "password"
    data = {"email": email, "password": password}
    r = client.post(
        "/api/v1/accounts",
        headers=normal_account_token_headers,
        json=data,
    )
    assert r.status_code == 403
