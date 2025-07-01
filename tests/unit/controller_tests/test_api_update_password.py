from src.service.exceptions import UserNotFoundError, ForbiddenError, NothingToUpdateError


def test_update_password_success(client):
    test_client, mock_service = client
    password_data = {"password": "NewPassword123/"}
    
    mock_service.update_password.return_value = None

    response = test_client.patch("/users/1/password", json = password_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Password updated successfully"}


def test_update_password_forbidden(client):
    test_client, mock_service = client
    
    password_data = {"password": "NewPassword123/"}
    
    mock_service.update_password.side_effect = ForbiddenError("Forbidden")
    
    response = test_client.patch("/users/2/password", json = password_data)
    
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_update_password_not_found(client):
    test_client, mock_service = client

    password_data = {"password": "NewPassword123/"}
    
    mock_service.update_password.side_effect = UserNotFoundError("User not found")
    
    response = test_client.patch("/users/999/password", json = password_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_password_no_data(client):
    test_client, mock_service = client

    response = test_client.patch("/users/1/password", json = {"password": ""})
    
    assert response.status_code == 422
    mock_service.update_password.assert_not_called()


def test_update_password_service_level_validation_error(client):
    test_client, mock_service = client
   
    mock_service.update_password.side_effect = NothingToUpdateError("No password provided")

    response = test_client.patch("/users/1/password", json = {"password": "ValidPassword123/"})

    assert response.status_code == 400
    assert response.json() == {"detail": "No password provided"}
    mock_service.update_password.assert_called_once()