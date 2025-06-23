from pydantic import BaseModel, field_validator
import re


class UserValidator(BaseModel):
    user_name: str
    email: str
    
    @field_validator("user_name")
    def validate_user_name(cls, value: str) -> str:
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
    
    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        value = value.strip()
        
        if not value:
            raise ValueError("Email name cannot be empty")
        
        if " " in value:
            raise ValueError("Email name cannot contain spaces")
        
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
            raise ValueError("Invalid email format")
        
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", value):
            raise ValueError("Email must contain only Latin letters")
        
        return value