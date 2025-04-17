from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    name: str = Field(...)


class UserResponse(UserRequest):
    ip: str = Field(...)
    id: str = Field(...)


class MessageRequest(BaseModel):
    content: str = Field(...)


class MessageResponse(MessageRequest):
    id: int = Field(...)
    sender_id: int = Field(...)
    recipient_id: int = Field(...)
