from src.db.db_repository import create_user
from src.db.models import User


def test_create_user(db_session, user_data):
    user = create_user(db_session, user_data)

    # Проверяем, что пользователь вернулся с id
    assert user.id == 1
    assert user.user_name == user_data["user_name"]
    assert user.email == user_data["email"]
    assert user.password == user_data["password"]
    
    # Проверяем, что пользователь реально в базе
    user_from_db = db_session.query(User).filter_by(email=user_data["email"]).first()
    assert user_from_db is not None
    assert user_from_db.user_name == user_data["user_name"]