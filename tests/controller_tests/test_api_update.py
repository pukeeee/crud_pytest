import pytest


@pytest.mark.parametrize("updated_fields", 
    [
        {"user_name": "NewName"},
        {"email": "newemail@mail.com"},
        {"user_name": "NewName", "email": "newemail@mail.com"},
        {"email": "newemail@mail.com", "user_name": "NewName"}
])
def test_update_user(create_user, new_user_data, updated_fields):
    data, test_client, mock_repo = create_user
    
    id = data["id"]
    token = data["access_token"]
    
    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}
    mock_repo.update_user.return_value = {**updated_fields}
    
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.patch(f"/users/{id}", headers = headers, json = updated_fields)
    
    assert response.status_code == 200
    assert response.json()["message"] == "User updated"
    for field in updated_fields:
        assert response.json()["user"][field] == updated_fields[field]
    assert "password" not in response.json()
    assert "password" not in response.json()["user"]
    assert "access_token" not in response.json()
    assert "access_token" not in response.json()["user"]
    mock_repo.update_user.assert_called_once_with(id, updated_fields)