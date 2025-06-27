from fastapi import FastAPI, Depends, HTTPException
from src.component.user_repository import UserRepository
from src.dto.user import UserCreate, UserUpdate, PasswordUpdate
from src.auth.auth import generate_token, get_current_user

app = FastAPI()

def get_user_repository():
    return UserRepository()


# Создание юзера
@app.post("/users")
def create_user(
    user: UserCreate, 
    repo: UserRepository = Depends(get_user_repository)
):
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
def get_user(
    id: int, 
    current_user_id: int = Depends(get_current_user), 
    repo: UserRepository = Depends(get_user_repository)
):
    if id != current_user_id:
        raise HTTPException(status_code = 403, detail = "Forbidden")

    user = repo.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return {"user_name": user["user_name"], "email": user["email"]}


@app.patch("/users/{id}")
def update_user(
    id: int,
    user: UserUpdate,
    current_user_id: int = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repository)
):
    if id != current_user_id:
        raise HTTPException(status_code = 403, detail = "Forbidden")

    existing_user = repo.get_user_by_id(id)
    if not existing_user:
        raise HTTPException(status_code = 404, detail = "User not found")

    update_data = user.model_dump(exclude_unset = True)
    if not update_data:
        raise HTTPException(status_code = 400, detail = "No fields to update")

    updated_fields = repo.update_user(id, update_data)
    if not updated_fields:
        raise HTTPException(status_code = 500, detail = "Failed to update user")

    updated_fields.pop("password", None)

    return {"message": "User updated", "user": updated_fields}


@app.patch("/users/{id}/password")
def update_password(
    id: int,
    data: PasswordUpdate,
    current_user_id: int = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repository)
):
    if id != current_user_id:
        raise HTTPException(status_code = 403, detail = "Forbidden")

    existing_user = repo.get_user_by_id(id)
    if not existing_user:
        raise HTTPException(status_code = 404, detail = "User not found")

    update_data = data.password
    if not update_data:
        raise HTTPException(status_code = 400, detail = "No password provided")

    updated_fields = repo.update_password(id, data.password)
    if not updated_fields:
        raise HTTPException(status_code = 500, detail = "Failed to update password")

    return {"message": "Password updated successfully"}