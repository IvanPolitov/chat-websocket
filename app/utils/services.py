from fastapi import Depends
from db.base import get_db
from db.repos import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from utils.utils import decode_jwt, hash_password, verify_password
from schemas.user import User


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


def get_user_services(db: AsyncSession = Depends(get_db)):
    return UserServices(UserRepository(db))
