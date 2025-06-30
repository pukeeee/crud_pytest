from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    start_date: int
    status: bool

    model_config = ConfigDict(from_attributes=True)
