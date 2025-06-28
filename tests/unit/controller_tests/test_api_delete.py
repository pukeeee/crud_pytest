def test_delete_user(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}
    mock_repo.delete_user.return_value = True

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.delete(f"/users/{id}", headers = headers)

    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}


def test_delete_user_forbidden(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    other_id = data["id"] + 1
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}
    mock_repo.delete_user.return_value = True

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.delete(f"/users/{other_id}", headers = headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


def test_delete_user_not_found(create_user):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = None

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.delete(f"/users/{id}", headers = headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_internal_error(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}
    mock_repo.delete_user.return_value = False

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.delete(f"/users/{id}", headers = headers)

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to delete user"


def test_delete_user_unauthorized(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    id = data["id"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}

    response = test_client.delete(f"/users/{id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"