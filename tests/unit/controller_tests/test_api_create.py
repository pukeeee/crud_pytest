import pytest
from src.service.exceptions import EmailAlreadyExistsError


def test_create_user_success(client, new_user_data):
    test_client, mock_service = client

    mock_service.create_user.return_value = (
        {"id": 1, "user_name": "Name", "email": "email@mail.com"},
        "access_token"
    )

    response = test_client.post("/users", json = new_user_data)
    data = response.json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["user_name"] == new_user_data["user_name"]
    assert "password" not in data
    assert data["access_token"] == "access_token"


def test_create_user_duplicate_email(client, new_user_data):
    test_client, mock_service = client

    mock_service.create_user.side_effect = EmailAlreadyExistsError("Email already exists")

    response = test_client.post("/users", json = new_user_data)
    data = response.json()

    assert response.status_code == 409
    assert "access_token" not in data
    assert data["detail"] == "Email already exists"
    mock_service.create_user.assert_called_once()


@pytest.mark.parametrize("field", ["user_name", "email", "password"])
def test_create_user_missing_field(client, new_user_data, field):
    test_client, _ = client

    missing_data = new_user_data.copy()
    missing_data.pop(field)

    response = test_client.post("/users", json = missing_data)
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data


def test_create_user_invalid_name(client, new_user_data):
    test_client, _ = client

    invalid_name = new_user_data.copy()
    invalid_name["user_name"] = "Bob"

    response = test_client.post("/users", json = invalid_name)
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data


def test_create_user_invalid_email(client, new_user_data):
    test_client, _ = client

    invalid_email = new_user_data.copy()
    invalid_email["email"] = "mail@mail"

    response = test_client.post("/users", json = invalid_email)
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data


def test_create_user_invalid_password(client, new_user_data):
    test_client, _ = client

    invalid_password = new_user_data.copy()
    invalid_password["password"] = "password"

    response = test_client.post("/users", json = invalid_password)
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data


def test_create_user_empty_body(client):
    test_client, _ = client

    response = test_client.post("/users", json = {})
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data