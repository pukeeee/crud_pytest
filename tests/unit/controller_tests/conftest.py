import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.controller.user_controller import app, get_user_service, get_current_user
from src.service.user_service import UserService


USER_ID = 1  # Константа для ID текущего пользователя во всех тестах


@pytest.fixture
def mock_user_service():
    """Создает мок для UserService c правильной спецификацией."""
    return MagicMock(spec = UserService)


@pytest.fixture
def client(mock_user_service):
    """
    Создает тестовый клиент, подменяя реальный сервис и аутентификацию
    на моки для полной изоляции контроллера.
    """
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    app.dependency_overrides[get_current_user] = lambda: USER_ID

    with TestClient(app) as test_client:
        yield test_client, mock_user_service
    
    # Очищаем подмены после теста, чтобы не влиять на другие тесты
    app.dependency_overrides.clear()


@pytest.fixture
def new_user_data():
    """Тестовые данные для создания пользователя."""
    return {
        "user_name": "Name", 
        "email": "email@mail.com", 
        "password": "Password123/"
    }


@pytest.fixture
def updated_user_data():
    """Тестовые данные для обновления пользователя."""
    return {
        "user_name": "NewName", 
        "email": "newemail@mail.com"
    }