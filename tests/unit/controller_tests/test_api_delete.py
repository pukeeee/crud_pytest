from src.service.exceptions import UserNotFoundError, ForbiddenError, InternalError


def test_delete_user_success(client):
    test_client, mock_service = client
    user_id_to_delete = 1

    mock_service.delete_user.return_value = None

    response = test_client.delete(f"/users/{user_id_to_delete}")

    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
    mock_service.delete_user.assert_called_once_with(user_id_to_delete, 1)


def test_delete_user_not_found(client):
    test_client, mock_service = client
    user_id_to_delete = 999
    
    mock_service.delete_user.side_effect = UserNotFoundError("User not found")

    response = test_client.delete(f"/users/{user_id_to_delete}")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_other_user_forbidden(client):
    test_client, mock_service = client
    user_id_to_delete = 2

    mock_service.delete_user.side_effect = ForbiddenError("Forbidden")

    response = test_client.delete(f"/users/{user_id_to_delete}")

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_delete_user_internal_error(client):
    test_client, mock_service = client
    user_id_to_delete = 1
    
    mock_service.delete_user.side_effect = InternalError("Failed to delete user")

    response = test_client.delete(f"/users/{user_id_to_delete}")

    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to delete user"}