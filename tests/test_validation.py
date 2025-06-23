import pytest
from src.validators import UserValidator
from contextlib import nullcontext as not_raises
from pydantic import ValidationError


@pytest.mark.parametrize(
    "user_name, exp",
    [
        ("name", not_raises()),
        ("Даня", not_raises()),
        ("  name  ", not_raises()),
        ("nam", pytest.raises(ValidationError, match = "User name must be longer than 3 characters")),
        (123, pytest.raises(ValidationError, match = "Input should be a valid string")),
        ("", pytest.raises(ValidationError, match = "User name cannot be empty")),
        (" ", pytest.raises(ValidationError, match = "User name cannot be empty")),
        ("qwertyqwertyqwertyqwe", pytest.raises(ValidationError, match = "User name must be less than 20 characters")),
        ("name/", pytest.raises(ValidationError, match = "User name can only contain letters")),
        ("name12", pytest.raises(ValidationError, match = "User name can only contain letters")),
        ("na me", pytest.raises(ValidationError, match = "User name cannot contain spaces"))
    ]
)
def test_user_name_validation(user_name, exp):
    with exp:
        UserValidator(user_name = user_name, email = "valid@mail.com")


@pytest.mark.parametrize(
    "email, exp",
    [
        ("mail@mail.com", not_raises()),
        ("  mail@mail.com  ", not_raises()),
        ("mail.mail@mail.com", not_raises()),
        ("", pytest.raises(ValidationError, match = "Email name cannot be empty")),
        (" ", pytest.raises(ValidationError, match = "Email name cannot be empty")),
        ("mail @mail.com", pytest.raises(ValidationError, match = "Email name cannot contain spaces")),
        ("mailmail.com", pytest.raises(ValidationError, match = "Invalid email format")),
        ("mail@mailcom", pytest.raises(ValidationError, match = "Invalid email format")),
        ("mail@@mailcom", pytest.raises(ValidationError, match = "Invalid email format")),
        ("пошта@mail.com", pytest.raises(ValidationError, match = "Email must contain only Latin letters"))
    ]
)
def test_email_validation(email, exp):
    with exp:
        UserValidator(user_name = "ValidName", email = email)