from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import UserCreate
from app.db.crud import create_user, get_user_by_username


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
