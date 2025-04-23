from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordBearer
from schemas.schemas import UserRequest
from db.models import User
from db.base import get_db
from sqlalchemy.orm import Session


user_router = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

@user_router.post('/login')
def login_user(
    user: UserRequest,
    db: Session = Depends(get_db)
):
