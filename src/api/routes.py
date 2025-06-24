from fastapi import FastAPI, Depends, HTTPException
from api.api_repository import UserRepository
from src.validation import UserValidation
from src.api.auth import generate_token

app = FastAPI()

def get_user_repository():
    return UserRepository()


# Создание юзера
@app.post("/users")
def create_user(user: UserValidation, repo: UserRepository = Depends(get_user_repository)):
    # Проверка на существующий email
    existing_email = repo.get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code = 409, detail = "Email already exists")

    user_data = repo.create_user(user.model_dump())
    access_token = generate_token(user_data["id"])

    user_data.pop("password", None)  # Удаление пароля из ответа

    return {
        **user_data,
        "access_token": access_token
    }


@app.get("/users/{user_id}")
def get_user(user_id: str, repo: UserRepository = Depends(get_user_repository)):
    user = repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user
