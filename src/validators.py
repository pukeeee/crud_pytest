from pydantic import BaseModel, field_validator
import re


class UserNameValidator(BaseModel):
    user_name: str
    
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
