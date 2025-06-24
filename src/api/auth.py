from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

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
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    
    except (JWTError, ValueError):
        raise ValueError("Invalid token")