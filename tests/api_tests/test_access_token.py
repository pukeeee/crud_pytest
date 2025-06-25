from src.api.auth import generate_token, verify_token
import pytest
from datetime import datetime, timezone, timedelta
from jose import jwt
from src.api.auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def test_generate_access_token():
    user_id = 1
    token = generate_token(user_id)

    assert len(token) > 0
    assert isinstance(token, str)
    assert verify_token(token) == user_id


@pytest.mark.parametrize("user_id",[
    (1),
    (100),
    (999999)
])
def test_generate_token_different_user_ids(user_id):
    token = generate_token(user_id)
    assert verify_token(token) == user_id


def test_token_invalid_user_id():
    token = generate_token("invalid_user_id")

    with pytest.raises(ValueError, match = "Invalid token"):
        verify_token(token)


@pytest.mark.parametrize("invalid_token", [
    ("invalidToken"),
    ("not.a.valid.token"),
    ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"),
    (""),
    ("   ")
])
def test_invalid_access_token(invalid_token):
    token = invalid_token
    
    with pytest.raises(ValueError, match = "Invalid token"):
        verify_token(token)


@pytest.mark.parametrize("bad_token", [None, 123, 1.5, [], {}])
def test_token_wrong_type(bad_token):
    with pytest.raises(ValueError, match = "Invalid token format"):
        verify_token(bad_token)


def test_token_expiry_is_correct():
    user_id = 123
    before = datetime.now(timezone.utc)

    token = generate_token(user_id)
    
    after = datetime.now(timezone.utc)
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    exp = datetime.fromtimestamp(payload["exp"], timezone.utc)

    # Нижняя и верхняя границы допустимого срока действия
    min_expected_exp = before + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) - timedelta(seconds = 5)
    max_expected_exp = after + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) + timedelta(seconds = 5)

    assert min_expected_exp < exp < max_expected_exp


def test_expired_token():
    expired_time = datetime.now(timezone.utc) - timedelta(minutes = 1)

    payload = {
        "sub": "123",
        "exp": expired_time
    }

    expired_token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

    with pytest.raises(ValueError, match = "Token has expired"):
        verify_token(expired_token)