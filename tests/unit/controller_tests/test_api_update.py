from fastapi.testclient import TestClient
from src.controller.user_controller import app
from src.service.exceptions import UserNotFoundError, ForbiddenError, EmailAlreadyExistsError, NothingToUpdateError, InternalError



def test_update_user_success(client, updated_user_data):
    """Тест успешного обновления своего профиля."""
    # Arrange
    test_client, mock_service = client
    user_id_to_update = 1
    expected_user = {"id": 1, **updated_user_data}
    mock_service.update_user.return_value = expected_user

    # Act
    response = test_client.patch(f"/users/{user_id_to_update}", json=updated_user_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "User updated", "user": expected_user}


def test_update_user_not_found(client, updated_user_data):
    """Тест обновления несуществующего пользователя."""
    test_client, mock_service = client
    mock_service.update_user.side_effect = UserNotFoundError("User not found")
    response = test_client.patch("/users/999", json=updated_user_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_other_user_forbidden(client, updated_user_data):
    """Тест попытки обновить чужой профиль."""
    test_client, mock_service = client
    mock_service.update_user.side_effect = ForbiddenError("Forbidden")
    response = test_client.patch("/users/2", json=updated_user_data)
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_update_unauthorized_user(updated_user_data):
    """Тест обновления без токена аутентификации."""
    with TestClient(app) as unauthenticated_client:
        response = unauthenticated_client.patch("/users/1", json=updated_user_data)
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"


def test_update_user_no_fields(client):
    """Тест обновления без полей в теле запроса."""
    test_client, mock_service = client
    mock_service.update_user.side_effect = NothingToUpdateError("No fields to update")
    response = test_client.patch("/users/1", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "No fields to update"}


def test_update_user_internal_error(client, updated_user_data):
    """Тест внутренней ошибки при обновлении."""
    test_client, mock_service = client
    mock_service.update_user.side_effect = InternalError("DB error")
    response = test_client.patch("/users/1", json=updated_user_data)
    assert response.status_code == 500
    assert response.json() == {"detail": "DB error"}


def test_update_user_duplicate_email(client, updated_user_data):
    """Тест обновления на уже занятый email."""
    test_client, mock_service = client
    mock_service.update_user.side_effect = EmailAlreadyExistsError("Email already exists")
    response = test_client.patch("/users/1", json=updated_user_data)
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already exists"}