from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from db.crud import create_user, add_user_to_room, get_user_by_username, create_room, get_rooms_by_user_id, get_room_by_name
from schemas.room import RoomCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: UserCreate):
        """
        Асинхронно создаёт нового пользователя, делегируя выполнение функции :func:`create_user`.

        Parameters
        ----------
        user_data : app.schemas.UserCreate
            Данные пользователя, полученные через Pydantic-модель.

        Returns
        -------
        app.models.User
            Объект созданного пользователя, возвращённый из функции :func:`create_user`.
        """
        return await create_user(self.db, user_data)

    async def get_by_username(self, username: str):
        return await get_user_by_username(self.db, username)


class RoomRepository:
    def __init__(self, db=AsyncSession):
        self.db = db

    async def create(self, room_data: RoomCreate):
        return await create_room(self.db, room_data)

    async def add_user(self, room_id: int, user_id: int):
        return await add_user_to_room(self.db, room_id, user_id)

    async def get_by_current_user_id(self, user_id: int):
        return await get_rooms_by_user_id(self.db, user_id)

    async def get_by_name(self, name: str):
        return await get_room_by_name(self.db, name)
