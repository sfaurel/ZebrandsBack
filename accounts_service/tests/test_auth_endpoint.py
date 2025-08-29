from fastapi.testclient import TestClient
from conftest import TEST_ACCOUNT


def test_login_fail(client: TestClient) -> None:
    wrong_credentials = {
        "email": "wrong_email@example.com",
        "password": "wrong_pass"
    }

    response = client.post("/api/v1/login", json=wrong_credentials)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_success(client: TestClient, test_account) -> None:
    credentials = {
        "email": test_account.email,
        "password": TEST_ACCOUNT.password
    }

    response = client.post("/api/v1/login", json=credentials)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 3600
