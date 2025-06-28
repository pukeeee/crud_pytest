import pytest
from dto.user import UserCreate
from contextlib import nullcontext as not_raises
from pydantic import ValidationError


@pytest.mark.parametrize("password, exp", 
    [
        ("Valid1/aW", not_raises()),
        ("ValidPassword123456/", not_raises()),
        ("ValidPassword1/", not_raises()),
        ("ValidPassword1!@", not_raises()),
        (None, pytest.raises(ValidationError)),
        (12345678, pytest.raises(ValidationError, match = "Input should be a valid string")),
        ("", pytest.raises(ValidationError, match = "Password cannot be empty")),
        ("         ", pytest.raises(ValidationError, match = "Password cannot be empty")),
        ("Short1/", pytest.raises(ValidationError, match = "Password must be longer than 8 characters")),
        ("VeryLongPassword1234567890/", pytest.raises(ValidationError, match = "Password must be less than 20 characters")),
        ("validpassword1/", pytest.raises(ValidationError, match = "Password must contain at least one uppercase letter")),
        ("VALIDPASSWORD1/", pytest.raises(ValidationError, match = "Password must contain at least one lowercase letter")),
        ("ValidPassword/", pytest.raises(ValidationError, match = "Password must contain at least one digit")),
        ("ValidPassword1", pytest.raises(ValidationError, match = "Password must contain at least one special character")),
        ("Valid Password1/", pytest.raises(ValidationError, match = "Password cannot contain spaces")),
        ("!!!!!!!!!!", pytest.raises(ValidationError, match = "Password must contain at least one uppercase letter")),
        ("validpassword/", pytest.raises(ValidationError, match = "Password must contain at least one uppercase letter")),
        ("ValidPassword1?", pytest.raises(ValidationError, match="Password must contain at least one special character")),
        ("ValidПароль1/", not_raises()),
        ("ValidPassword1\n", pytest.raises(ValidationError, match="Password must contain at least one special character")),
    ]
)
def test_password_validation(password, exp):
    with exp:
        UserCreate(user_name = "ValidName", email = "valid@mail.com", password = password)