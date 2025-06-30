from src.service.exceptions import UserNotFoundError, ForbiddenError, NothingToUpdateError


def test_update_password_success(client):
    """Тест успешного обновления пароля."""
    # Arrange
    test_client, mock_service = client
    password_data = {"password": "NewPassword123/"}
    mock_service.update_password.return_value = None  # Сервис ничего не возвращает в случае успеха

    # Act
    response = test_client.patch("/users/1/password", json=password_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Password updated successfully"}


def test_update_password_forbidden(client):
    """Тест попытки сменить пароль другому пользователю."""
    test_client, mock_service = client
    password_data = {"password": "NewPassword123/"}
    mock_service.update_password.side_effect = ForbiddenError("Forbidden")
    response = test_client.patch("/users/2/password", json=password_data)
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_update_password_not_found(client):
    """Тест смены пароля несуществующему пользователю."""
    test_client, mock_service = client
    password_data = {"password": "NewPassword123/"}
    mock_service.update_password.side_effect = UserNotFoundError("User not found")
    response = test_client.patch("/users/999/password", json=password_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_password_no_data(client):
    """Тест смены пароля без передачи данных (пустая строка)."""
    test_client, mock_service = client

    response = test_client.patch("/users/1/password", json={"password": ""})
    
    # Ожидаем 422, потому что Pydantic-модель не пропустит пустой пароль
    assert response.status_code == 422
    
    # Убеждаемся, что наш сервис не был вызван
    mock_service.update_password.assert_not_called()


def test_update_password_service_level_validation_error(client):
    """Тест ошибки 400, когда сервис получает недопустимые данные,
       которые пропустил Pydantic (гипотетический случай)."""
    test_client, mock_service = client
    mock_service.update_password.side_effect = NothingToUpdateError("No password provided")

    # Act
    response = test_client.patch("/users/1/password", json={"password": "ValidPassword123/"})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "No password provided"}
    # Убеждаемся, что сервис был вызван
    mock_service.update_password.assert_called_once()