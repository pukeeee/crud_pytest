import pytest
from validation import UserCreate
from contextlib import nullcontext as not_raises
from pydantic import ValidationError


@pytest.mark.parametrize("user_name, exp",
    [
        ("name", not_raises()),
        ("Даня", not_raises()),
        ("  name  ", not_raises()),
        (None, pytest.raises(ValidationError)),
        ("nam", pytest.raises(ValidationError, match = "User name must be longer than 3 characters")),
        (123, pytest.raises(ValidationError, match = "Input should be a valid string")),
        ("", pytest.raises(ValidationError, match = "User name cannot be empty")),
        (" ", pytest.raises(ValidationError, match = "User name cannot be empty")),
        ("qwertyqwertyqwertyqwe", pytest.raises(ValidationError, match = "User name must be less than 20 characters")),
        ("name/", pytest.raises(ValidationError, match = "User name can only contain letters")),
        ("name12", pytest.raises(ValidationError, match = "User name can only contain letters")),
        ("na me", pytest.raises(ValidationError, match = "User name cannot contain spaces")),
    ]
)
def test_user_name_validation(user_name, exp):
    with exp:
        UserCreate(user_name = user_name, email = "valid@mail.com", password = "ValidPassword1/")


@pytest.mark.parametrize("email, exp",
    [
        ("mail@mail.com", not_raises()),
        ("  mail@mail.com  ", not_raises()),
        ("mail.mail@mail.com", not_raises()),
        (None, pytest.raises(ValidationError)),
        (123, pytest.raises(ValidationError, match = "Input should be a valid string")),
        ("", pytest.raises(ValidationError, match = "Email name cannot be empty")),
        (" ", pytest.raises(ValidationError, match = "Email name cannot be empty")),
        ("mail @mail.com", pytest.raises(ValidationError, match = "Email name cannot contain spaces")),
        ("mailmail.com", pytest.raises(ValidationError, match = "Invalid email format")),
        ("mail@mailcom", pytest.raises(ValidationError, match = "Invalid email format")),
        ("mail@@mailcom", pytest.raises(ValidationError, match = "Invalid email format")),
        ("пошта@mail.com", pytest.raises(ValidationError, match = "Email must contain only Latin letters")),
        ("mailmailmailmail@mailmail.comco", pytest.raises(ValidationError, match = "Email name must be less than 30 characters"))
    ]
)
def test_email_validation(email, exp):
    with exp:
        UserCreate(user_name = "ValidName", email = email, password = "ValidPassword1/")


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