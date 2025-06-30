from fastapi.testclient import TestClient
from src.controller.user_controller import app
from src.service.exceptions import UserNotFoundError, ForbiddenError


def test_get_user_profile_success(client, new_user_data):
    """Тест успешного получения своего профиля."""
    # Arrange
    test_client, mock_service = client
    user_id_to_get = 1  # Запрашиваем свой профиль
    
    # Настраиваем мок-сервис на возврат данных пользователя
    expected_user = {"user_name": new_user_data["user_name"], "email": new_user_data["email"]}
    mock_service.get_user.return_value = expected_user

    # Act
    response = test_client.get(f"/users/{user_id_to_get}")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_user
    # Проверяем, что метод сервиса был вызван с правильными ID
    mock_service.get_user.assert_called_once_with(user_id_to_get, 1)


def test_get_user_not_found(client):
    """Тест получения несуществующего пользователя."""
    # Arrange
    test_client, mock_service = client
    user_id_to_get = 999
    
    # Настраиваем мок-сервис на выброс исключения
    mock_service.get_user.side_effect = UserNotFoundError("User not found")

    # Act
    response = test_client.get(f"/users/{user_id_to_get}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_other_user_forbidden(client):
    """Тест попытки получения чужого профиля."""
    # Arrange
    test_client, mock_service = client
    other_user_id = 2 # ID другого пользователя
    
    # Настраиваем мок-сервис на выброс исключения
    mock_service.get_user.side_effect = ForbiddenError("Forbidden")

    # Act
    response = test_client.get(f"/users/{other_user_id}")

    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_get_user_unauthorized():
    """Тест доступа без токена аутентификации."""
    # Arrange
    with TestClient(app) as unauthenticated_client:
        user_id = 1
        
        # Act
        response = unauthenticated_client.get(f"/users/{user_id}")

        # Assert
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"