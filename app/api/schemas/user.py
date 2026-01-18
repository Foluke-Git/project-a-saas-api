from pydantic import BaseModel, EmailStr, Field
from pydantic import field_validator
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    def strip_password(cls, v: str) -> str:
        return v.strip()


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_verified: bool

class Config:
    from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None