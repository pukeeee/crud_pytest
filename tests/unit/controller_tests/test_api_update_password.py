import pytest


@pytest.mark.parametrize("updated_password", 
    [
        {"password": "NewPassword123/"}
])
def test_update_user_password(create_user, updated_password):
    data, test_client, mock_repo = create_user
    
    id = data["id"]
    token = data["access_token"]
    
    mock_repo.update_password.return_value = {**updated_password}
    
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.patch(f"/users/{id}/password", headers = headers, json = updated_password)
    
    assert response.status_code == 200
    assert response.json() == {"message": "Password updated successfully"}
    assert "password" not in response.json()
    assert "access_token" not in response.json()
    mock_repo.update_password.assert_called_once_with(id, updated_password["password"])