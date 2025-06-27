# from fastapi.testclient import TestClient
# from src.api.routes import app, get_user_repository
# from unittest.mock import MagicMock
# import pytest


def test_get_user_profile_success(create_user, new_user_data):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = {"id": id, **new_user_data}

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get(f"/users/{id}", headers = headers)

    assert response.status_code == 200
    assert response.json()["user_name"] == new_user_data["user_name"]
    assert response.json()["email"] == new_user_data["email"]
    assert "access_token" not in response.json()
    assert "password" not in response.json()


def test_get_user_not_found(create_user):
    data, test_client, mock_repo = create_user

    id = data["id"]
    token = data["access_token"]

    mock_repo.get_user_by_id.return_value = None

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get(f"/users/{id}", headers = headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_forbidden(create_user):
    data, test_client, _ = create_user

    other_id = 2
    token = data["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get(f"/users/{other_id}", headers = headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


def test_get_unauthorized_user(create_user):
    data, test_client, _ = create_user

    id = data["id"]

    response = test_client.get(f"/users/{id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"