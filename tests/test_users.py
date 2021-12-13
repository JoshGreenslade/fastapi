import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_user(client):
    new_user_request = {"email": "user@example.com", "password": "password123"}
    response = client.post("/users/", json=new_user_request)

    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "user@example.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.auth_secret_key,
        algorithms=[settings.auth_algorithm],
    )
    id = payload.get("user_id")

    assert response.status_code == 200
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@example.com", "password123", 403),
        ("user@example.com", "WrongPasswod", 403),
        ("wrongemail@example.com", "WrongPassword", 403),
        (None, "password123", 422),
        ("user@example.com", None, 422),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
    )

    assert response.status_code == status_code
