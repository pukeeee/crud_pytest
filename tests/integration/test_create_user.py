from src.db.models import User


def test_create_user_integration(db_session, user_data, client):
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    # Проверяем, что пользователь реально в базе
    user = db_session.query(User).filter_by(email=user_data["email"]).first()
    assert user is not None
    assert user.user_name == user_data["user_name"]
    assert user.email == user_data["email"]