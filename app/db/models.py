from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Text
from db.base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    ip: Mapped[str] = mapped_column(String, nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(Text)
