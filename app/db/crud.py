from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import User, Room, RoomParticipant
from schemas.user import UserCreate
from schemas.room import RoomCreate


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """ """
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_room_by_name(db: AsyncSession, name: str) -> Room | None:
    """ """
    result = await db.execute(select(Room).where(Room.name == name))
    return result.scalars().first()


async def get_rooms_by_user_id(db: AsyncSession, user_id: int) -> Room | None:
    """ """

    result = await db.execute(select(Room).join(RoomParticipant, Room.id == RoomParticipant.room_id).where(RoomParticipant.user_id == user_id))

    return result.scalars().all()


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


async def create_room(db: AsyncSession, room_data: RoomCreate) -> Room:
    """ """
    db_room = Room(**room_data.model_dump())
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room


async def add_user_to_room(db: AsyncSession, room_id: int, user_id: int):
    db_room = await db.execute(select(Room).where(Room.id == room_id))
    db_room = db_room.scalars().first()
    db_user = await db.execute(select(User).where(User.id == user_id))
    db_user = db_user.scalars().first()
    participant = RoomParticipant(user_id=db_user.id, room_id=db_room.id)
    db.add(participant)
    await db.commit()
    await db.refresh(db_room)
    return db_room
