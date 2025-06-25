# from fastapi.testclient import TestClient
# from src.api.routes import app, get_user_repository
# from unittest.mock import MagicMock
# import pytest


def test_get_user_profile_success(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user.return_value = {"id": id, **new_user_data}

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get(f"/users/{id}", headers = headers)

    assert response.status_code == 200
    assert response.json() == {
        "user_name": new_user_data["user_name"],
        "email": new_user_data["email"]
    }
    assert "access_token" and "password" not in response.json()


def test_get_user_not_found(create_user):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user.return_value = None

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get(f"/users/{id}", headers = headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"