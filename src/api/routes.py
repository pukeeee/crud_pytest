from fastapi import FastAPI, Depends, HTTPException
from api.api_repository import UserRepository
from src.validation import UserCreate
from src.api.auth import generate_token, get_current_user

app = FastAPI()

def get_user_repository():
    return UserRepository()


# Создание юзера
@app.post("/users")
def create_user(user: UserCreate, repo: UserRepository = Depends(get_user_repository)):
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


@app.get("/users/{id}")
def get_user(id: int, current_user_id: int = Depends(get_current_user), repo: UserRepository = Depends(get_user_repository)):
    if id != current_user_id:
        raise HTTPException(status_code = 403, detail = "Forbidden")

    user = repo.get_user(id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return {"user_name": user["user_name"], "email": user["email"]}


@app.patch("/users/{id}")
def edit_user(id: int, current_user_id: int = Depends(get_current_user), repo: UserRepository = Depends(get_user_repository)):
    # Проверка авторизации
    if id != current_user_id:
        raise HTTPException(status_code = 403, detail = "Forbidden")
    
    # Проверка существования пользователя
    user = repo.get_user(id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    # Если ничего не передано для обновления
    if not any(user.user_name, user.email, user.password):
        raise HTTPException(status_code = 400, detail = "No fields to update")