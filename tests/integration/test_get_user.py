def test_get_user_integration(user_data, client):
    create_response = client.post("/users", json = user_data)
    assert create_response.status_code == 201

    created_user = create_response.json()
    user_id = created_user["id"]
    access_token = created_user["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    get_response = client.get(f"/users/{user_id}", headers = headers)
    assert get_response.status_code == 200

    user = get_response.json()
    assert user["user_name"] == user_data["user_name"]
    assert user["email"] == user_data["email"]
    assert "password" not in user