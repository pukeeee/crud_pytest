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


def test_update_user_not_found(create_user, updated_user_data):
    data, test_client, mock_repo = create_user
    
    id = data["id"]
    token = data["access_token"]
    
    mock_repo.get_user_by_id.return_value = None

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.patch(f"/users/{id}", headers = headers, json = updated_user_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_forbidden(create_user, updated_user_data, new_user_data):
    data, test_client, mock_repo = create_user

    other_id = data["id"] + 1
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.patch(f"/users/{other_id}", headers = headers, json = updated_user_data)

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


def test_update_unauthorized_user(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    id = data["id"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}

    response = test_client.patch(f"/users/{id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_update_user_no_fields(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.patch(f"/users/{id}", headers = headers, json = {})

    assert response.status_code == 400
    assert response.json()["detail"] == "No fields to update"


def test_update_user_internal_error(create_user, new_user_data, updated_user_data):
    data, test_client, mock_repo = create_user
    
    id = data["id"]
    token = data["access_token"]
    
    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}
    mock_repo.update_user.return_value = None

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.patch(f"/users/{id}", headers = headers, json = updated_user_data)

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to update user"


def test_update_user_duplicate_email(create_user, new_user_data):
    data, test_client, mock_repo = create_user
    
    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}
    mock_repo.get_user_by_email.return_value = {"id": id + 1, "email": "taken@mail.com"}

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.patch(f"/users/{id}", headers = headers, json = {"email": "taken@mail.com"})

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"