import pytest
from dto.user import UserCreate
from contextlib import nullcontext as not_raises
from pydantic import ValidationError


@pytest.mark.parametrize("email, exp",
    [
        ("mail@mail.com", not_raises()),
        ("  mail@mail.com  ", not_raises()),
        ("mail.mail@mail.com", not_raises()),
        (None, pytest.raises(ValidationError)),
        (123, pytest.raises(ValidationError, match = "Input should be a valid string")),
        ("", pytest.raises(ValidationError, match = "Email cannot be empty")),
        (" ", pytest.raises(ValidationError, match = "Email cannot be empty")),
        ("mail @mail.com", pytest.raises(ValidationError, match = "Email cannot contain spaces")),
        ("mailmail.com", pytest.raises(ValidationError, match = "Invalid email format")),
        ("mail@mailcom", pytest.raises(ValidationError, match = "Invalid email format")),
        ("mail@@mailcom", pytest.raises(ValidationError, match = "Invalid email format")),
        ("пошта@mail.com", pytest.raises(ValidationError, match = "Email must contain only Latin letters")),
        ("mailmailmailmail@mailmail.comco", pytest.raises(ValidationError, match = "Email must be less than 30 characters"))
    ]
)
def test_email_validation(email, exp):
    with exp:
        UserCreate(user_name = "ValidName", email = email, password = "ValidPassword1/")