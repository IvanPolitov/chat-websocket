from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, mapped_column, Mapped, DeclarativeBase

URL_DB = 'sqlite:///./chat.db'

engine = create_engine(url=URL_DB, connect_args={'check_same_thread': False})
get_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
