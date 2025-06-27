from pydantic import BaseModel, field_validator
import re


class UserValidation(BaseModel):
    @staticmethod
    def validate_user_name(value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("User name cannot be empty")
        if len(value) < 4:
            raise ValueError("User name must be longer than 3 characters")
        if len(value) > 20:
            raise ValueError("User name must be less than 20 characters")
        if " " in value:
            raise ValueError("User name cannot contain spaces")
        if not re.match(r"^[A-Za-zА-Яа-яЁё]+$", value):
            raise ValueError("User name can only contain letters")
        return value

    @staticmethod
    def validate_email(value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Email cannot be empty")
        if " " in value:
            raise ValueError("Email cannot contain spaces")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
            raise ValueError("Invalid email format")
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", value):
            raise ValueError("Email must contain only Latin letters")
        if len(value) > 30:
            raise ValueError("Email must be less than 30 characters")
        return value

    @staticmethod
    def validate_password(value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Password cannot be empty")
        if " " in value:
            raise ValueError("Password cannot contain spaces")
        if len(value) < 9:
            raise ValueError("Password must be longer than 8 characters")
        if len(value) > 20:
            raise ValueError("Password must be less than 20 characters")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*()_+=/-]", value):
            raise ValueError("Password must contain at least one special character (!@#$%^&*()_+=-/)")
        return value


class UserCreate(UserValidation):
    user_name: str
    email: str
    password: str

    @field_validator("user_name")
    def validate_user_name_field(cls, value):
        return cls.validate_user_name(value)

    @field_validator("email")
    def validate_email_field(cls, value):
        return cls.validate_email(value)

    @field_validator("password")
    def validate_password_field(cls, value):
        return cls.validate_password(value)


class UserUpdate(UserValidation):
    user_name: str | None = None
    email: str | None = None

    @field_validator("user_name")
    def validate_user_name_field(cls, value):
        if value is None:
            return value
        return cls.validate_user_name(value)

    @field_validator("email")
    def validate_email_field(cls, value):
        if value is None:
            return value
        return cls.validate_email(value)


class PasswordUpdate(UserValidation):
    password: str

    @field_validator("password")
    def validate_password_field(cls, value):
        return cls.validate_password(value)