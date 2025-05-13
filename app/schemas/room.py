from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from schemas.message import MessageInRoom



class RoomBase(BaseModel):
    name: str = Field(...)


class RoomRequest(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int = Field(...)


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int = Field(...)
    messages: Optional[List[MessageInRoom]] = []
    created_at: datetime = Field(...)
    participants: List[int] = []

    class Config:
        orm_mode = True
