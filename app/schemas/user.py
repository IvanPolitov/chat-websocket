from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(...)
    role: Optional[str] = Field(default='common_user')


class UserRequest(UserBase):
    pass


class UserResponse(UserBase):
    id: int = Field(...)


class UserCreate(UserBase):
    password: str = Field(...)


class User(UserBase):
    id: int = Field(...)
    password: str = Field(...)
    created_at: datetime = Field(...)

    class Config:
        orm_mode = True
