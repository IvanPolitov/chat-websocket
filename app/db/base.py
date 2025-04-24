from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession

URL_DB = 'sqlite+aiosqlite:///./chat.db'

engine = create_async_engine(url=URL_DB)
get_session = async_sessionmaker(bind=engine, expire_on_commit=True)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.

    Этот класс наследует `AsyncAttrs` и `DeclarativeBase`, что позволяет использовать асинхронные операции
    с атрибутами моделей. Также он определяет общее поле `created_at` для всех таблиц.

    Attributes
    ----------
    created_at : Mapped[datetime]
        Дата и время создания записи. Значение устанавливается автоматически при создании записи в базе данных.
    """
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


async def get_db() -> AsyncSession:
    """
    Асинхронный контекстный менеджер для получения сессии базы данных.

    Используется для управления жизненным циклом сессии базы данных. После завершения работы сессия
    автоматически закрывается.

    Yields
    ------
    AsyncSession
        Асинхронная сессия базы данных.
    """
    async with get_session() as session:
        yield session


async def create_db():
    """
    Создает все таблицы в базе данных.

    Использует метаданные базового класса `Base` для создания всех таблиц, определенных в моделях.
    Операция выполняется асинхронно через соединение с базой данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """
    Удаляет все таблицы из базы данных.

    Использует метаданные базового класса `Base` для удаления всех таблиц, определенных в моделях.
    Операция выполняется асинхронно через соединение с базой данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
