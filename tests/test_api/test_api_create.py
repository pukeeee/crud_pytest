from fastapi.testclient import TestClient
from src.api.routes import app, get_user_repository
from unittest.mock import MagicMock
import pytest


@pytest.fixture(scope = "function")
def client():
    # Создание мок-репозитория для подмены реального слоя данных
    mock_repo = MagicMock()
    # Переопределение зависимости FastAPI на мок-репозиторий
    app.dependency_overrides[get_user_repository] = lambda: mock_repo

    return TestClient(app), mock_repo


@pytest.fixture
def valid_user():
    return {
        "user_name": "Name", 
        "email": "email@mail.com", 
        "password": "Password123/"
    }


def test_create_user_success(client, valid_user):
    test_client, mock_repo = client

    mock_repo.get_user_by_email.return_value = None
    mock_repo.create_user.return_value = {"id": 1, **valid_user}
    response = test_client.post("/users", json=valid_user)
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["user_name"] == valid_user["user_name"]
    assert data["email"] == valid_user["email"]
    assert "password" not in data
    assert "access_token" in data


@pytest.mark.parametrize("field", ["user_name", "email", "password"])
def test_create_user_missing_field(client, valid_user, field):
    test_client, _ = client

    missing_data = valid_user.copy()
    missing_data.pop(field)

    response = test_client.post("/users", json = missing_data)
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data


def test_create_user_invalid_name(client, valid_user):
    test_client, _ = client

    invalid_name = valid_user.copy()
    invalid_name["user_name"] = "Bob"

    response = test_client.post("/users", json = invalid_name)
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data


def test_create_user_invalid_email(client, valid_user):
    test_client, _ = client

    invalid_email = valid_user.copy()
    invalid_email["email"] = "mail@mail"

    response = test_client.post("/users", json = invalid_email)
    data = response.json()

    assert response.status_code == 422
    assert "access_token" not in data


def test_create_user_invalid_password(client, valid_user):
    test_client, _ = client

    invalid_password = valid_user.copy()
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


def test_create_user_duplicate_email(client, valid_user):
    test_client, mock_repo = client

    mock_repo.get_user_by_email.return_value = {"id": 1, **valid_user}
    response = test_client.post("/users", json = valid_user)
    data = response.json()

    assert response.status_code == 409
    assert "access_token" not in data
    assert data["detail"] == "Email already exists"