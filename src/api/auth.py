from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Header, HTTPException


SECRET_KEY = "dotenv"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def generate_token(user_id: int) -> str:
    """Создание JWT-токена"""
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    
    return token


def verify_token(token: str) -> int:
    """Проверка JWT-токена и извлечение user_id"""
    if not isinstance(token, str) or not token.strip():
        raise ValueError("Invalid token format")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    
    except ExpiredSignatureError:
        raise ValueError("Token has expired")

    except (JWTError, ValueError):
        raise ValueError("Invalid token")


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> int:
    """Извлекает user_id из токена в заголовке Authorization"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code = 401, detail = "Unauthorized")
    
    token = authorization.split(" ")[1]
    
    try:
        user_id = verify_token(token)
        return user_id
    except (JWTError, ValueError):
        raise HTTPException(status_code = 401, detail = "Invalid token")