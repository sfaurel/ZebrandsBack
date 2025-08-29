from fastapi.testclient import TestClient
from sqlmodel import Session
import uuid

from app.services.account_service import create_account
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

# TODO: check why this test make someothers tests fail
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


def test_create_account_by_normal_account(
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

# TODO: check why this test make someothers tests fail
# def test_update_account(
#     client: TestClient,
#     admin_account_token_headers: dict[str, str],
#     db: Session
# ) -> None:
#     email = "new_email@example.com"
#     password = "password"
#     account_in = AccountCreate(email=email, password=password)
#     account = create_account(session=db, account_create=account_in)

#     data = {"full_name": "Updated_full_name"}
#     response = client.patch(
#         f"/api/v1/accounts/{account.id}",
#         headers=admin_account_token_headers,
#         json=data,
#     )
#     assert response.status_code == 200
#     updated_account = response.json()

#     assert updated_account["full_name"] == "Updated_full_name"

#     account_query = select(Account).where(Account.email == email)
#     account_db = db.exec(account_query).first()
#     db.refresh(account_db)
#     assert account_db
#     assert account_db.full_name == "Updated_full_name"


# def test_update_account_by_normal_account(
#     client: TestClient,
#     admin_account_token_headers: dict[str, str],
#     db: Session
# ) -> None:
#     email = "by_normal_user@example.com"
#     password = "password"
#     account_in = AccountCreate(email=email, password=password)
#     account = create_account(session=db, account_create=account_in)

#     data = {"full_name": "Updated_full_name"}
#     response = client.patch(
#         f"/api/v1/accounts/{account.id}",
#         headers=admin_account_token_headers,
#         json=data,
#     )
#     assert response.status_code == 403


def test_update_account_not_exists(
    client: TestClient, admin_account_token_headers: dict[str, str]
) -> None:
    data = {"full_name": "Updated_full_name"}
    response = client.patch(
        f"/api/v1/accounts/{uuid.uuid4()}",
        headers=admin_account_token_headers,
        json=data,
    )
    assert response.status_code == 404
    assert response.json()[
        "detail"] == "The account with this id does not exist in the system"


def test_update_account_email_exists(
    client: TestClient,
    admin_account_token_headers: dict[str, str],
    db: Session
) -> None:
    email = "existing_email@example.com"
    password = "password"
    account_in = AccountCreate(email=email, password=password)
    account = create_account(session=db, account_create=account_in)

    email2 = "another_existing_email@example.com"
    password2 = "password"
    account_in2 = AccountCreate(email=email2, password=password2)
    account2 = create_account(session=db, account_create=account_in2)

    data = {"email": account2.email}
    response = client.patch(
        f"/api/v1/accounts/{account.id}",
        headers=admin_account_token_headers,
        json=data,
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Account with this email already exists"
