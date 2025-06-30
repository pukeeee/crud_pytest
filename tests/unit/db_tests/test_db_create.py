from src.db.db_repository import DatabaseUserRepository
from src.db.models import User


def test_create_user(db_session, user_data):
    repo = DatabaseUserRepository(db_session)
    user_dict = repo.create_user(user_data)

    # Проверяем, что пользователь вернулся с id
    assert user_dict["id"] is not None
    assert user_dict["user_name"] == user_data["user_name"]
    assert user_dict["email"] == user_data["email"]
    assert "password" not in user_dict # Убеждаемся, что пароль не возвращается

    # Проверяем, что пользователь реально в базе
    user_from_db = db_session.query(User).filter_by(email=user_data["email"]).first()
    assert user_from_db is not None
    assert user_from_db.user_name == user_data["user_name"]