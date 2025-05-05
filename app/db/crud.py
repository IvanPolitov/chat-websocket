from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import User
from schemas.user import UserCreate


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Асинхронно создаёт нового пользователя в базе данных.

    Parameters
    ----------
    db : AsyncSession
        Асинхронная сессия SQLAlchemy для взаимодействия с БД.
    user_data : UserCreate
        Данные нового пользователя, полученные через Pydantic-модель.

    Returns
    -------
    User
        Созданный экземпляр модели пользователя после сохранения в БД.

    Notes
    -----
    Функция:
    1. Создаёт запись в БД.
    2. Сохраняет данные асинхронно.
    3. Обновляет объект из БД, чтобы получить актуальные данные (например, id).
    """
    db_user = User(**user_data.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
