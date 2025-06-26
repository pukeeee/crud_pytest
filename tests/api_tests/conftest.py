from fastapi.testclient import TestClient
from src.api.routes import app, get_user_repository
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def client():
    # Создание мок-репозитория для подмены реального слоя данных
    mock_repo = MagicMock()
    # Переопределение зависимости FastAPI на мок-репозиторий
    app.dependency_overrides[get_user_repository] = lambda: mock_repo

    return TestClient(app), mock_repo


@pytest.fixture
def new_user_data():
    return {
        "user_name": "Name", 
        "email": "email@mail.com", 
        "password": "Password123/"
    }


@pytest.fixture
def create_user(client, new_user_data):
    """Создаёт пользователя и возвращает (response.json, client, mock_repo)"""
    test_client, mock_repo = client

    # Мокаем создание пользователя
    mock_repo.get_user_by_email.return_value = None
    mock_repo.create_user.return_value = {"id": 1, **new_user_data}

    create_response = test_client.post("/users", json = new_user_data)
    assert create_response.status_code == 200

    data = create_response.json()

    return data, test_client, mock_repo