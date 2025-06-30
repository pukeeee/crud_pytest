from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.component.user_repository import UserRepository
from src.db.models import User
from src.dto.user_response import UserResponse
from src.service.exceptions import EmailAlreadyExistsError


def to_dict(user: User) -> dict:
    """Преобразует объект User в словарь, соответствующий UserResponse."""
    return UserResponse.model_validate(user).model_dump()


class DatabaseUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db


    def create_user(self, user_data: dict) -> dict:
        user = User(**user_data)
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return to_dict(user)
        except IntegrityError as e:
            self.db.rollback()
            raise EmailAlreadyExistsError("Email already exists") from e


    def get_user_by_email(self, email: str) -> dict | None:
        statement = select(User).where(User.email == email)
        user = self.db.execute(statement).scalar_one_or_none()
        return to_dict(user) if user else None


    def get_user_by_id(self, id: int) -> dict | None:
        user = self.db.get(User, id)
        return to_dict(user) if user else None


    def update_user(self, id: int, user_data: dict) -> dict | None:
        if not user_data:
            return self.get_user_by_id(id)
        
        statement = update(User).where(User.id == id).values(**user_data).returning(User)
        result = self.db.execute(statement).scalar_one_or_none()
        self.db.commit()
        
        return to_dict(result) if result else None


    def update_password(self, id: int, password: str) -> dict | None:
        statement = update(User).where(User.id == id).values(password=password).returning(User)
        result = self.db.execute(statement).scalar_one_or_none()
        self.db.commit()
        return to_dict(result) if result else None


    def delete_user(self, id: int) -> bool:
        user = self.db.get(User, id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
