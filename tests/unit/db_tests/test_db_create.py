from src.db.db_repository import DatabaseUserRepository
from src.db.models import User
from src.service.exceptions import EmailAlreadyExistsError
import pytest


def test_create_user(db_session, user_data):
    repo = DatabaseUserRepository(db_session)
    user_dict = repo.create_user(user_data)

    assert user_dict["id"] is not None
    assert user_dict["user_name"] == user_data["user_name"]
    assert user_dict["email"] == user_data["email"]
    assert "password" not in user_dict


    user_from_db = db_session.query(User).filter_by(email = user_data["email"]).first()
    assert user_from_db is not None
    assert user_from_db.user_name == user_data["user_name"]


def test_create_user_existing_email(db_session, user_data):
    repo = DatabaseUserRepository(db_session)
    repo.create_user(user_data)
    
    with pytest.raises(EmailAlreadyExistsError):
        repo.create_user(user_data)