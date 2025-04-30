from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(...)


class UserRequest(UserBase):
    pass


class UserResponse(UserBase):
    id: int = Field(...)


class UserCreate(UserBase):
    password: str = Field(...)


class User(UserBase):
    id: int = Field(...)
    password_hashed: str = Field(...)
    created_at: datetime = Field(...)

    class Config:
        orm_mode = True


class MassageBase(BaseModel):
    room_id: int = Field(...)


class MessageCreate(BaseModel):
    content: str = Field(...)
    room_id: str = Field(...)


class MessageRequest(BaseModel):
    content: str = Field(...)
    sender_id: int = Field(...)


class Message(MassageBase):
    id: int = Field(...)
    sender_id: int = Field(...)
    created_at: datetime = Field(...)
    content: str = Field(...)

    class Config:
        orm_mode = True
