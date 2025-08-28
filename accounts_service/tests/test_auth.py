from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_fail():
    credentials = {
        "email": "wrong_email@example.com",
        "password": "wrong_pass"
    }

    response = client.post("/api/v1/login", json=credentials)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}