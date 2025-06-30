from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.component.user_repository import UserRepository
from src.db.db_repository import DatabaseUserRepository
from src.db.database import SessionLocal
from src.dto.user import UserCreate, UserUpdate, PasswordUpdate
from src.auth.auth import get_current_user
from src.service.user_service import UserService
from src.service.exceptions import UserNotFoundError, EmailAlreadyExistsError, ForbiddenError, NothingToUpdateError, InternalError

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return DatabaseUserRepository(db)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


@app.post("/users", status_code=201)
def create_user(
    user: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    """Создает нового пользователя и возвращает его данные с токеном доступа."""
    try:
        user_data, access_token = service.create_user(user)
        return {**user_data, "access_token": access_token}
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/users/{id}")
def get_user(
    id: int, 
    current_user_id: int = Depends(get_current_user), 
    service: UserService = Depends(get_user_service)
):
    """Возвращает публичные данные пользователя по его ID."""
    try:
        user = service.get_user(id, current_user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.patch("/users/{id}")
def update_user(
    id: int,
    user_update: UserUpdate,
    current_user_id: int = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """Обновляет данные пользователя (имя, email)."""
    try:
        updated_user = service.update_user(id, current_user_id, user_update)
        return {"message": "User updated", "user": updated_user}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NothingToUpdateError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InternalError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/users/{id}/password")
def update_password(
    id: int,
    password_data: PasswordUpdate,
    current_user_id: int = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """Обновляет пароль пользователя."""
    try:
        service.update_password(id, current_user_id, password_data)
        return {"message": "Password updated successfully"}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except NothingToUpdateError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InternalError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/{id}")
def delete_user(
    id: int,
    current_user_id: int = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    """Удаляет пользователя."""
    try:
        service.delete_user(id, current_user_id)
        return {"message": "User deleted successfully"}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except InternalError as e:
        raise HTTPException(status_code=500, detail=str(e))