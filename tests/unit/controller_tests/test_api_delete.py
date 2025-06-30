from src.service.exceptions import UserNotFoundError, ForbiddenError, InternalError


def test_delete_user_success(client):
    # Arrange
    test_client, mock_service = client
    user_id_to_delete = 1  # Удаляем сами себя

    # Настраиваем мок-сервис: метод delete_user не возвращает ничего в случае успеха
    mock_service.delete_user.return_value = None

    # Act
    response = test_client.delete(f"/users/{user_id_to_delete}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
    # Проверяем, что метод сервиса был вызван с правильными аргументами
    mock_service.delete_user.assert_called_once_with(user_id_to_delete, 1)


def test_delete_user_not_found(client):
    # Arrange
    test_client, mock_service = client
    user_id_to_delete = 999
    
    # Настраиваем мок-сервис на выброс исключения
    mock_service.delete_user.side_effect = UserNotFoundError("User not found")

    # Act
    response = test_client.delete(f"/users/{user_id_to_delete}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_other_user_forbidden(client):
    # Arrange
    test_client, mock_service = client
    user_id_to_delete = 2  # Пытаемся удалить другого пользователя

    # Настраиваем мок-сервис на выброс исключения
    mock_service.delete_user.side_effect = ForbiddenError("Forbidden")

    # Act
    response = test_client.delete(f"/users/{user_id_to_delete}")

    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_delete_user_internal_error(client):
    # Arrange
    test_client, mock_service = client
    user_id_to_delete = 1
    
    # Настраиваем мок-сервис на выброс исключения
    mock_service.delete_user.side_effect = InternalError("Failed to delete user")

    # Act
    response = test_client.delete(f"/users/{user_id_to_delete}")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to delete user"}