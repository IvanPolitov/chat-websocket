from datetime import datetime
from pydantic import BaseModel, Field


class MassageBase(BaseModel):
    room_id: int = Field(...)


class MessageCreate(BaseModel):
    content: str = Field(...)
    room_id: str = Field(...)


class MessageRequest(BaseModel):
    content: str = Field(...)
    sender_id: int = Field(...)


class MessageInRoom(BaseModel):
    id: int = Field(...)
    created_at: datetime = Field(...)
    sender_id: int = Field(...)
    content: str = Field(...)


class Message(MassageBase):
    id: int = Field(...)
    sender_id: int = Field(...)
    created_at: datetime = Field(...)
    content: str = Field(...)

    class Config:
        orm_mode = True
