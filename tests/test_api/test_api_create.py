from fastapi.testclient import TestClient
from src.api.routes import app, get_user_repository
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def user_data():
    return {
        "user_name": "Name", 
        "email": "email@mail.com", 
        "password": "Password123/"
    }


def test_create_user_success(user_data):
    mock_repo = MagicMock() # Создаем мок-репозиторий для подмены реального слоя данных
    mock_repo.create_user.return_value = {"id": 1, **user_data}

    app.dependency_overrides[get_user_repository] = lambda: mock_repo # Переопределяем зависимость FastAPI на мок-репозиторий

    client = TestClient(app) # Создаем тестовый клиент для отправки запросов к API
    response = client.post("/users", json = user_data)

    assert response.status_code == 200
    assert response.json() == {"id": 1, **user_data}
    mock_repo.create_user.assert_called_once_with(user_data)