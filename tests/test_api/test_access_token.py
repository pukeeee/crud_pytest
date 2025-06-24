from src.api.auth import generate_token, verify_token
import pytest


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