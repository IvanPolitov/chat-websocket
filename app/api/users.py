from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repos import UserRepository
from app.utils.services import UserServices
from schemas.schemas import UserRequest
from db.base import get_db
from sqlalchemy.orm import Session


user_router = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


def get_user_services(db: AsyncSession = Depends(get_db)):
    return UserServices(UserRepository(db))


@user_router.post('/login')
def login_user(
    user: UserRequest,
    db: Session = Depends(get_db)
):
