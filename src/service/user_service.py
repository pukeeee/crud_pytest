from src.component.user_repository import UserRepository
from src.dto.user import UserCreate, UserUpdate, PasswordUpdate
from src.auth.auth import generate_token
from src.auth.hash import hash_password
from src.service.exceptions import UserNotFoundError, EmailAlreadyExistsError, ForbiddenError, NothingToUpdateError, InternalError


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo


    def create_user(self, user_data: UserCreate) -> tuple[dict, str]:
        if self.repo.get_user_by_email(user_data.email):
            raise EmailAlreadyExistsError("Email already exists")
        
        user_dict = user_data.model_dump()
        user_dict["password"] = hash_password(user_dict["password"])
        
        created_user = self.repo.create_user(user_dict)
        access_token = generate_token(created_user["id"])

        return created_user, access_token


    def get_user(self, user_id: int, current_user_id: int) -> dict:
        if user_id != current_user_id:
            raise ForbiddenError("Forbidden")
        
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        return {"user_name": user["user_name"], "email": user["email"]}


    def update_user(self, user_id: int, current_user_id: int, update_data: UserUpdate) -> dict:
        if user_id != current_user_id:
            raise ForbiddenError("Forbidden")

        # Проверяем, существует ли пользователь, которого пытаемся обновить
        if not self.repo.get_user_by_id(user_id):
            raise UserNotFoundError("User not found")

        # Проверяем, не занят ли новый email другим пользователем
        if update_data.email:
            existing_email_user = self.repo.get_user_by_email(update_data.email)
            if existing_email_user and existing_email_user.get("id") != user_id:
                raise EmailAlreadyExistsError("Email already exists")
        
        user_dict = update_data.model_dump(exclude_unset=True)
        if not user_dict:
            raise NothingToUpdateError("No fields to update")

        updated_user = self.repo.update_user(user_id, user_dict)
        if not updated_user:
            # Это может произойти если, например, id не был найден в момент самого апдейта
            raise InternalError("Failed to update user")
        
        updated_user.pop("password", None)
        return updated_user


    def update_password(self, user_id: int, current_user_id: int, password_data: PasswordUpdate) -> None:
        if user_id != current_user_id:
            raise ForbiddenError("Forbidden")
        if not self.repo.get_user_by_id(user_id):
            raise UserNotFoundError("User not found")
        if not password_data.password:
            raise NothingToUpdateError("No password provided")
        hashed = hash_password(password_data.password)
        if not self.repo.update_password(user_id, hashed):
            raise InternalError("Failed to update password")


    def delete_user(self, user_id: int, current_user_id: int) -> None:
        if user_id != current_user_id:
            raise ForbiddenError("Forbidden")
        
        if not self.repo.get_user_by_id(user_id):
            raise UserNotFoundError("User not found")
        
        deleted_user = self.repo.delete_user(user_id)
        if not deleted_user:
            raise InternalError("Failed to delete user")