from fastapi import FastAPI, Depends, HTTPException
from src.api.repository import UserRepository
from src.validation import UserValidation

app = FastAPI()

def get_user_repository():
    return UserRepository()


# Создание юзера
@app.post("/users")
def create_user(user: UserValidation, repo: UserRepository = Depends(get_user_repository)):
    return repo.create_user(user.model_dump())

@app.get("/users/{user_id}")
def get_user(user_id: str, repo: UserRepository = Depends(get_user_repository)):
    user = repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user
