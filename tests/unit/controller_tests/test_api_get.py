from fastapi.testclient import TestClient
from src.controller.user_controller import app
from src.service.exceptions import UserNotFoundError, ForbiddenError


def test_get_user_profile_success(client, new_user_data):
    test_client, mock_service = client
    user_id_to_get = 1
    
    expected_user = {"user_name": new_user_data["user_name"], "email": new_user_data["email"]}
    mock_service.get_user.return_value = expected_user

    response = test_client.get(f"/users/{user_id_to_get}")

    assert response.status_code == 200
    assert response.json() == expected_user
    mock_service.get_user.assert_called_once_with(user_id_to_get, 1)


def test_get_user_not_found(client):
    test_client, mock_service = client
    user_id_to_get = 999
    
    mock_service.get_user.side_effect = UserNotFoundError("User not found")

    response = test_client.get(f"/users/{user_id_to_get}")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_other_user_forbidden(client):
    test_client, mock_service = client
    other_user_id = 2
    
    mock_service.get_user.side_effect = ForbiddenError("Forbidden")

    response = test_client.get(f"/users/{other_user_id}")

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_get_user_unauthorized():
    with TestClient(app) as unauthenticated_client:
        user_id = 1
        
        response = unauthenticated_client.get(f"/users/{user_id}")

        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"