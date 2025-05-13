from fastapi import Depends
from db.base import get_db
from db.repos import UserRepository, RoomRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, User
from schemas.room import RoomCreate, Room
from utils.utils import decode_jwt, hash_password, verify_password
from typing import List


class UserServices:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> User:
        user_data.password = hash_password(user_data.password)
        return await self.user_repo.create(user_data)

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repo.get_by_username(username)

        if not user or not verify_password(user.password, password):
            return None
        return user

    async def unique_user(self, username: str) -> bool:
        user = await self.user_repo.get_by_username(username)
        if user:
            return False
        return True

    async def get_user_from_token(self, token: str) -> User:
        payload = decode_jwt(token)
        user = await self.user_repo.get_by_username(payload.get('sub'))

        return user


class RoomServices:
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo

    async def create_room(self, room_data: RoomCreate, creator_id: int) -> Room:
        new_room = await self.room_repo.create(room_data)
        new_room = await self.room_repo.add_user(new_room.id, creator_id)
        return new_room

    async def get_all_current_user_rooms(self, user_id: int) -> List[Room]:
        rooms = await self.room_repo.get_by_current_user_id(user_id)
        return rooms

    async def unique_room(self, name: str) -> bool:
        room = await self.room_repo.get_by_name(name)
        if room:
            return False
        return True


def get_user_services(db: AsyncSession = Depends(get_db)):
    return UserServices(UserRepository(db))


def get_room_services(db: AsyncSession = Depends(get_db)):
    return RoomServices(RoomRepository(db))
