import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.controller.user_controller import app, get_user_service, get_current_user
from src.service.user_service import UserService


USER_ID = 1  # Константа для ID поточного користувача у всіх тестах


@pytest.fixture
def mock_user_service():
    """Створює мок для UserService з правильною специфікацією."""
    return MagicMock(spec = UserService)


@pytest.fixture
def client(mock_user_service):
    """
    Створює тестовий клієнт, підміняючи реальний сервіс та автентифікацію
    на моки для повної ізоляції контролера.
    """
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    app.dependency_overrides[get_current_user] = lambda: USER_ID

    with TestClient(app) as test_client:
        yield test_client, mock_user_service
    
    # Очищаємо підміни після тесту, щоб не впливати на інші тести
    app.dependency_overrides.clear()


@pytest.fixture
def new_user_data():
    """Тестові дані для створення користувача."""
    return {
        "user_name": "Name", 
        "email": "email@mail.com", 
        "password": "Password123/"
    }


@pytest.fixture
def updated_user_data():
    """Тестові дані для оновлення користувача."""
    return {
        "user_name": "NewName", 
        "email": "newemail@mail.com"
    }