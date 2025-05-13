from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Text
from db.base import Base


class RoomParticipant(Base):
    __tablename__ = 'room_participants'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('rooms.id'), primary_key=True)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True,  nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)

    participated_rooms = relationship(
        "Room", 
        secondary="room_participants", 
        back_populates="participants"
    )

    


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('rooms.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    room = relationship("Room", back_populates="messages")


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    participants = relationship(
        "User", 
        secondary="room_participants", 
        back_populates="participated_rooms"
    )

    messages = relationship("Message", back_populates="room")

